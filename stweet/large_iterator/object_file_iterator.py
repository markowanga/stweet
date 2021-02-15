"""Iterator of objects in file."""
from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Optional, Iterator, List

from .file_lines_iterator import FileLinesIterator

T = TypeVar('T')


class ObjectFileIterator(Generic[T], ABC, Iterator):
    """Iterator of objects in file."""

    file_path: str
    lines_iterator: Optional[FileLinesIterator]
    chunk_size: int

    def __init__(self, file_path: str, chunk_size: int):
        """Constructor of ObjectFileIterator."""
        self.file_path = file_path
        self.lines_iterator = None
        self.chunk_size = chunk_size

    def open(self):
        """Method opens fileIterator."""
        if self.lines_iterator is None:
            self.lines_iterator = FileLinesIterator(self.file_path)
            self.lines_iterator.open()

    def close(self):
        """Method close fileIterator."""
        if self.lines_iterator is not None:
            self.lines_iterator.close()

    @abstractmethod
    def _parse_line(self, line: str) -> T:
        """Abstract method to parse line to object."""

    def __next__(self) -> List[T]:
        """Iterator method next."""
        lines = []
        counter = 0
        last = None
        while counter < self.chunk_size and (counter == 0 or last is not None):
            counter = counter + 1
            last = self.lines_iterator.next_line()
            if last is not None:
                lines.append(last)
        if len(lines) == 0:
            raise StopIteration
        return [self._parse_line(line) for line in lines]
