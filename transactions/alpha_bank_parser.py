from datetime import datetime

from transactions.domain_models import TransactionData, TransactionCategoryEnum


class AlphaBankTransactionsParser:
    @classmethod
    def parse_csv(cls, csv_file_path: str) -> list[TransactionData]:
        """
        Parses a CSV file and creates a list of transaction records.

        Raises `FileNotFoundError` if the given file path does not exist.
        """
        transactions = []

        with open(csv_file_path, "r") as f:
            for i, line in enumerate(f.readlines()):
                if i == 0:  # skip header
                    continue

                transactions.append(cls._parse_line(line))

        return transactions

    @staticmethod
    def _parse_line(csv_line: str) -> TransactionData:
        fields = csv_line.split(";")
        d = datetime.strptime(fields[1], "%d/%m/%Y").date()
        description = fields[2].strip('="')
        transaction_number = fields[5].strip('="')
        amount = float(fields[-3].replace(",", "."))
        amount = -amount if fields[-2] == "Χ" else amount
        category_id = TransactionCategoryEnum.create_from_description(description).value
        return TransactionData(
            date=d,
            description=description,
            transaction_number=transaction_number,
            amount=amount,
            category_id=category_id,
        )
