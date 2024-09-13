from typing import TypedDict, Iterable
from datetime import date
from enum import Enum


class TransactionCategoryEnum(Enum):
    SUPER_MARKET = 1
    RENT = 2
    WATER_BILL = 3
    POWER_BILL = 4
    INTERNET_BILL = 5
    PHONE_BILL = 6
    PAYROLL = 7
    BOOKS = 8
    HOBBIES = 9
    CASH_WITHDRAWAL = 10
    OTHER = 11
    HOUSE_FACILITIES_BILL = 12

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
    date: date
    description: str
    transaction_number: str
    amount: float
