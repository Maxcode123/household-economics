from datetime import date
from dataclasses import dataclass


@dataclass
class monthyear:
    _date: date

    @property
    def month(self) -> int:
        return self._date.month

    @property
    def year(self) -> int:
        return self._date.year

    def __hash__(self) -> int:
        return hash(str(self.month) + str(self.year))
