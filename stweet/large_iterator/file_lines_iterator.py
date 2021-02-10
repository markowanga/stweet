from typing import Optional


class FileLinesIterator:
    _file_path: str
    _file: any
    _file_iterator: any

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._file = None

    def open(self):
        self._file = open(self._file_path, 'r')

    def close(self):
        if self._file is not None:
            self._file.close()

    def next_line(self) -> Optional[str]:
        line = next(self._file)
        return line[:-1] if len(line) > 0 else None
