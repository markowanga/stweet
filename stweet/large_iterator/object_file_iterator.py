from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Optional

from .file_lines_iterator import FileLinesIterator

T = TypeVar('T')


class ObjectFileIterator(Generic[T], ABC):
    file_path: str
    lines_iterator: Optional[FileLinesIterator]

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lines_iterator = None

    def open(self):
        if self.lines_iterator is None:
            self.lines_iterator = FileLinesIterator(self.file_path)
            self.lines_iterator.open()

    def close(self):
        if self.lines_iterator is not None:
            self.lines_iterator.close()

    @abstractmethod
    def _parse_line(self, line: str) -> T:
        """Abstract method to parse line to object."""

    def next(self) -> Optional[T]:
        line = self.lines_iterator.next_line()
        return self._parse_line(line) if line is not None else None
