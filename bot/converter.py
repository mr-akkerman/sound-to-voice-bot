import logging
import os
import subprocess

logger = logging.getLogger(__name__)


class ConversionError(Exception):
    """Raised when MP3 → OGG conversion fails."""


def convert_mp3_to_ogg(input_path: str, output_path: str) -> None:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    try:
        result = subprocess.run(
            ["ffmpeg", "-i", input_path, "-c:a", "libopus", "-y", output_path],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise ConversionError(
            f"ffmpeg failed (exit {exc.returncode}): {exc.stderr.decode()}"
        ) from exc

    logger.info("Converted %s -> %s", input_path, output_path)
