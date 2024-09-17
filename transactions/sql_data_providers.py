"""
This module defines objects that execute custom sql queries and serve the data.

If you need data that is not in a Model and want to use that data in a domain model,
define a provider here.
"""

from decimal import Decimal
from typing import TypeAlias

from django.db import connection

from transactions.domain_models import (
    TransactionStatistics,
    MonthlyTransactionStatistics,
    TransactionCategoryEnum,
)
from utils.monthyear import monthyear

DbRow: TypeAlias = tuple[Decimal, Decimal, Decimal, Decimal, Decimal, Decimal]


class MonthlyTransactionStatisticsProvider:
    @classmethod
    def get_monthly_transaction_statistics(
        cls,
    ) -> list[MonthlyTransactionStatistics]:
        """
        Gets the summarized monthly statistics for the transactions within the given
        time period.
        """
        with connection.cursor() as cursor:
            cursor.execute(
                cls._get_query(),
                params=[
                    list(
                        map(
                            lambda c: c["id"], TransactionCategoryEnum.bill_categories()
                        )
                    ),
                    list(
                        map(
                            lambda c: c["id"],
                            TransactionCategoryEnum.leisure_categories(),
                        )
                    ),
                ],
            )
            rows = cursor.fetchall()

        monthly_stats = sorted(
            cls._parse_query_result(rows), key=lambda s: s.monthyear, reverse=True
        )
        return monthly_stats

    @staticmethod
    def _get_query() -> str:
        return """
            SELECT
                received.month,
                received.year,
                received.total_received,
                spent.total_spent,
                spent_bills.total_spent_in_bills,
                spent_leisure.total_spent_in_leisure
            FROM
            (
                (
                    SELECT
                        SUM(amount) AS total_received,
                        EXTRACT(MONTH FROM date) AS month,
                        EXTRACT(YEAR FROM date) AS year
                    FROM transactions
                    WHERE amount >= 0
                    GROUP BY EXTRACT(MONTH FROM date), EXTRACT(YEAR FROM date)
                ) AS received
                LEFT JOIN (
                    SELECT
                        (0 - SUM(amount)) AS total_spent,
                        EXTRACT(MONTH FROM date) AS month,
                        EXTRACT(YEAR FROM date) AS year
                    FROM transactions
                    WHERE amount < 0
                    GROUP BY EXTRACT(MONTH FROM date), EXTRACT(YEAR FROM date)
                ) AS spent
                ON received.month=spent.month AND received.year=spent.year
                LEFT JOIN (
                    SELECT
                        (0 - SUM(amount)) AS total_spent_in_bills,
                        EXTRACT(MONTH FROM date) AS month,
                        EXTRACT(YEAR FROM date) AS year
                    FROM transactions
                    WHERE amount < 0 AND category_id = ANY(%s)
                    GROUP BY EXTRACT(MONTH FROM date), EXTRACT(YEAR FROM date)
                ) AS spent_bills
                ON received.month=spent_bills.month AND received.year=spent_bills.year
                LEFT JOIN (
                    SELECT
                        (0 - SUM(amount)) AS total_spent_in_leisure,
                        EXTRACT(MONTH FROM date) AS month,
                        EXTRACT(YEAR FROM date) AS year
                    FROM transactions
                    WHERE amount < 0 AND category_id = ANY(%s)
                    GROUP BY EXTRACT(MONTH FROM date), EXTRACT(YEAR FROM date)
                ) AS spent_leisure
                ON received.month=spent_leisure.month AND received.year=spent_leisure.year
            )
        """

    @staticmethod
    def _parse_query_result(query_result: list[DbRow]) -> MonthlyTransactionStatistics:
        monthly_stats = []
        for row in query_result:
            my = monthyear(month=row[0], year=row[1])
            stats = TransactionStatistics(
                total_received=float(row[2]),
                total_spent=float(row[3]),
                total_spent_in_bills=float(row[4]),
                total_spent_in_leisure=float(row[5]),
            )
            monthly_stats.append(
                MonthlyTransactionStatistics(monthyear=my, stats=stats)
            )

        return monthly_stats
