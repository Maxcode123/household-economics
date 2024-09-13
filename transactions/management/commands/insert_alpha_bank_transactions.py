from django.core.management.base import BaseCommand, CommandError

from transactions.alpha_bank_parser import AlphaBankTransactionsParser
from transactions.models import Transaction


class Command(BaseCommand):
    help = "Insert Transaction records from Alpha Bank csv file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file_path", type=str)

    def handle(self, *args, **options):
        try:
            transaction_data = AlphaBankTransactionsParser.parse_csv(
                options["csv_file_path"]
            )
        except FileNotFoundError:
            raise CommandError(f'File {options["csv_file_path"]} was not found.')

        inserted = 0
        for data in transaction_data:
            if (
                Transaction.find_by_transaction_number(data["transaction_number"])
                is None
            ):
                Transaction(**data).save()
                inserted += 1

        self.stdout.write(self.style.SUCCESS(f"Inserted {inserted} records"))
