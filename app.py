from flask import Flask, render_template, request, redirect, url_for, Response
import os
import datetime
import csv
from detect import detect_objects

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

violations = []

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("video")

    if not file or file.filename == "":
        return "No file selected"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    violation_detected, violation_type, detected_image_path = detect_objects(filepath)

    if violation_detected:

        if violation_type == "No Helmet":
            fine_amount = 1000
        elif violation_type == "No Seatbelt":
            fine_amount = 500
        else:
            fine_amount = 0

        plate_number = "DEMO1234"

        violation_data = {
            "plate": plate_number,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fine": fine_amount,
            "type": violation_type,
            "image": detected_image_path
        }

        violations.append(violation_data)

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():

    total_violations = len(violations)
    total_fine = sum(v["fine"] for v in violations)

    helmet_count = sum(1 for v in violations if v["type"] == "No Helmet")
    seatbelt_count = sum(1 for v in violations if v["type"] == "No Seatbelt")

    return render_template(
        "dashboard.html",
        violations=violations,
        total_violations=total_violations,
        total_fine=total_fine,
        helmet_count=helmet_count,
        seatbelt_count=seatbelt_count
    )


@app.route("/export")
def export():
    def generate():
        data = [["Plate", "Time", "Fine", "Type"]]
        for v in violations:
            data.append([v["plate"], v["time"], v["fine"], v["type"]])

        for row in data:
            yield ",".join(map(str, row)) + "\n"

    return Response(generate(),
                    mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=report.csv"})


if __name__ == "__main__":
    app.run(debug=True)