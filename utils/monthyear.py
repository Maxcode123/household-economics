from dataclasses import dataclass
from calendar import month_name
from datetime import date


@dataclass
class monthyear:
    month: int
    year: int

    def __init__(self, month, year):
        try:
            self.month = int(month)
        except Exception:
            raise TypeError(
                f"could not create monthyear object with month: {month}; Expected integer. "
            )

        try:
            self.year = int(year)
        except Exception:
            raise TypeError(
                f"could not create monthyear object with year: {year}; Expected integer. "
            )

    def __repr__(self) -> str:
        return f"{month_name[self.month]} {self.year}"

    def __hash__(self) -> int:
        return hash(str(self.year) + str(self.month))

    def __gt__(self, other) -> bool:
        if not isinstance(other, monthyear):
            raise TypeError(
                f"> not supported between instances of 'monthyear' and {type(other)}"
            )

        return date(self.year, self.month, 1) > date(other.year, other.month, 1)
