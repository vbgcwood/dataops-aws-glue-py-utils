# validation_utils.py
import re
from .logging_utils import setup_logger

logger = setup_logger(__name__)


def verify_sanitized(_input: str | list[str], /, pattern: str = "") -> None:
    """
    Verifies that a string or list of strings is sanitized.
    Must match the pattern ^[a-zA-Z0-9_]+$ or a supplied override pattern.

    Parameters:
    - _input (str | list[str]): Text to validate sanitized.

    Key Arguments:
    - pattern (str): Regular expression pattern to match against.
    """
    if not pattern:
        pattern = re.compile(r"^[a-zA-Z0-9_]+$")
    else:
        logger.warning(f"Overriding default pattern with supplied pattern: '{pattern}'")

    def verify(s: str) -> str:
        if not isinstance(s, str):
            raise TypeError("Sanitation verification may only occur on strings.")

        if not pattern.match(s):
            invalid_chars = set(c for c in s if not (c.isalnum() or c == "_"))
            raise ValueError(
                f"Unsanitized Input! Invalid characters {invalid_chars} found in input: '{s}'"
            )
        return s

    if isinstance(_input, list):
        for item in _input:
            verify(item)
    elif isinstance(_input, str):
        verify(_input)
    else:
        raise TypeError(
            "Sanitation verification may only occur on strings or lists thereof."
        )
