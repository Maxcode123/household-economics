from typing import TypedDict, Iterable
from datetime import date
from enum import Enum
from dataclasses import dataclass

from utils.monthyear import monthyear


class TransactionCategoryEnum(Enum):
    """
    Maps transaction category records from DB.
    """

    SUPER_MARKET = {"id": 1, "name": "SUPER_MARKET"}
    RENT = {"id": 2, "name": "RENT"}
    WATER_BILL = {"id": 3, "name": "WATER_BILL"}
    POWER_BILL = {"id": 4, "name": "POWER_BILL"}
    INTERNET_BILL = {"id": 5, "name": "INTERNET_BILL"}
    PHONE_BILL = {"id": 6, "name": "PHONE_BILL"}
    PAYROLL = {"id": 7, "name": "PAYROLL"}
    BOOKS = {"id": 8, "name": "BOOKS"}
    HOBBIES = {"id": 9, "name": "HOBBIES"}
    CASH_WITHDRAWAL = {"id": 10, "name": "CASH_WITHDRAWAL"}
    OTHER = {"id": 11, "name": "OTHER"}
    HOUSE_FACILITIES_BILL = {"id": 12, "name": "HOUSE_FACILITIES_BILL"}

    @property
    def id(self) -> int:
        return self.value["id"]

    @property
    def name(self) -> str:
        return self.value["name"]

    @classmethod
    def bill_categories(cls) -> set[dict]:
        return {
            cls.RENT.value,
            cls.WATER_BILL.value,
            cls.POWER_BILL.value,
            cls.INTERNET_BILL.value,
            cls.PHONE_BILL.value,
            cls.HOUSE_FACILITIES_BILL.value,
        }

    @classmethod
    def leisure_categories(cls) -> set[dict]:
        return {cls.BOOKS, cls.HOBBIES, cls.OTHER}

    @classmethod
    def create_from_description(
        cls, transacion_description: str
    ) -> "TransactionCategoryEnum":
        """Create a category enum from a transaction description."""

        def is_in_description(strings: Iterable[str]):
            return any(map(lambda s: s in transacion_description, strings))

        if is_in_description(
            {
                "SUΡΕRMΑRΚΕΤ",
                "SUΡΕR ΜΑRΚΕΤ",
                "SΚLΑVΕΝΙΤΙS",
                "ΚRΙΤΙΚΟS",
                "ΜΑSΟUΤΙS",
                "ΑΒ_SΗΟΡ",
                "SΥΝ.ΚΑ",
                "SΥΝΚΑ",
                "ΜΑRΚΕΤ ΙΝ",
                "ΑΒ VΑSΙLΟΡΟULΟS",
            }
        ):
            return cls.SUPER_MARKET

        if is_in_description({"ΕΝΟΙΚΙΟ", "ΝΟΙΚΙ"}):
            return cls.RENT

        if is_in_description({"ΕΥDΑΡ"}):
            return cls.WATER_BILL

        if is_in_description({"ΝRG"}):
            return cls.POWER_BILL

        if is_in_description({"CΟSΜΟΤΕ FΙΧΕD"}):
            return cls.INTERNET_BILL

        if is_in_description({"CΟSΜΟΤΕ ΑVΤ"}):
            return cls.PHONE_BILL

        if is_in_description({"ΣΚΡΟΥΤΖ", "ΜΙΣΘΟΔΟΣΙΑ"}):
            return cls.PAYROLL

        if is_in_description({"ΑΝΑΛΗΨΗ ΑΠΟ"}):
            return cls.CASH_WITHDRAWAL

        return cls.OTHER


class TransactionData(TypedDict):
    """
    Holds the fields that represent a transaction in the business domain.
    """

    date: date
    description: str
    transaction_number: str
    amount: float


@dataclass
class MonthlyTransactionStatistics:
    """
    Contains summary statistics for all the transactions of a month.
    """

    monthyear: monthyear
    total_received: float
    total_spent: float
    total_spent_in_bills: float
    total_spent_in_leisure: float

    @property
    def savings(self) -> float:
        if self.received == 0:
            return 0

        return self.received - self.spent
