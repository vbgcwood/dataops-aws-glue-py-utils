# io_utils.py
import toml


def read_stripped_lines(file_path: str) -> list[str]:
    """
    Reads a file path line by line and returns a list of stripped lines.

    Parameters:
    - file_path (str): The file path to read.

    Returns:
    - list[str]: A list of stripped lines.
    """
    stripped_lines = []
    with open(file_path, "r") as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                stripped_lines.append(stripped_line)
    return stripped_lines


def read_toml(file_path: str) -> dict[str, any]:
    """
    Reads a TOML file and returns the data as a dictionary.

    Parameters:
    - file_path (str): The file path to read.

    Returns:
    - dict[str, any]: The data from the TOML file.
    """
    with open(file_path, "r") as f:
        data = toml.load(f)
    return data
