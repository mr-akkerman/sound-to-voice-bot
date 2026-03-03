import logging
import os

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

logger = logging.getLogger(__name__)


class ConversionError(Exception):
    """Raised when MP3 → OGG conversion fails."""


def convert_mp3_to_ogg(input_path: str, output_path: str) -> None:
    """Convert an MP3 file to OGG/Opus format.

    Args:
        input_path: Absolute or relative path to the source .mp3 file.
        output_path: Absolute or relative path for the resulting .ogg file.

    Raises:
        FileNotFoundError: If *input_path* does not exist.
        ConversionError: If pydub/ffmpeg fails to decode or encode the audio.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    try:
        audio = AudioSegment.from_mp3(input_path)
    except CouldntDecodeError as exc:
        raise ConversionError(f"Could not decode MP3: {input_path}") from exc
    except Exception as exc:
        raise ConversionError(f"Unexpected error while reading MP3: {exc}") from exc

    try:
        audio.export(output_path, format="ogg", codec="libopus")
    except Exception as exc:
        raise ConversionError(f"Could not export to OGG: {exc}") from exc

    logger.info("Converted %s -> %s", input_path, output_path)
