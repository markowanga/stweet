"""Iterator to get next file lines."""
from typing import Optional


class FileLinesIterator:
    """Iterator to get next file lines."""

    _file_path: str
    _file: any
    _file_iterator: any

    def __init__(self, file_path: str):
        """Constructor of FileLinesIterator."""
        self._file_path = file_path
        self._file = None

    def open(self):
        """Method to open file."""
        self._file = open(self._file_path, 'r')

    def close(self):
        """Method to close file."""
        if self._file is not None:
            self._file.close()

    def next_line(self) -> Optional[str]:
        """Next line method."""
        line = next(self._file)
        return line[:-1] if len(line) > 0 else None
