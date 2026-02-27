import React, { useState } from "react";

interface Props {
  src?: string;
  alt?: string;
  className?: string;
  style?: React.CSSProperties;
}

const ERROR_IMG_SRC =
  "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODgiIGhlaWdodD0iODgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgc3Ryb2tlPSIjMDAwIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBvcGFjaXR5PSIuMyIgZmlsbD0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIzLjciPjxyZWN0IHg9IjE2IiB5PSIxNiIgd2lkdGg9IjU2IiBoZWlnaHQ9IjU2IiByeD0iNiIvPjxwYXRoIGQ9Im0xNiA1OCAxNi0xOCAzMiAzMiIvPjxjaXJjbGUgY3g9IjUzIiBjeT0iMzUiIHI9IjciLz48L3N2Zz4=";

export default function ImageWithFallback({
  src,
  alt,
  className,
  style,
}: Props) {
  const [hasError, setHasError] = useState<boolean>(false);

  if (hasError) {
    return (
      <div className={className} style={style}>
        <img src={ERROR_IMG_SRC} alt="fallback" />
      </div>
    );
  }

  return (
    <img
      src={src ?? ""}
      alt={alt ?? "image"}
      className={className}
      style={style}
      onError={() => setHasError(true)}
    />
  );
}