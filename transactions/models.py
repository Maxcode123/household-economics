from typing import Optional

from django.db.models import (
    CharField,
    DateField,
    DecimalField,
    ForeignKey,
    SET_NULL,
    PositiveIntegerField,
)

from utils.base_model import BaseModel, register_admin


@register_admin
class TransactionCategory(BaseModel):
    """
    Transactions are classified by categories, e.g. RENT, PAYROLL, HOBBIES, SUPER_MARKET
    """

    id = PositiveIntegerField(primary_key=True, null=False)
    name = CharField(max_length=35)

    class Meta:
        db_table = "transaction_categories"


@register_admin
class Transaction(BaseModel):
    """
    A bank transaction, either incoming or outgoing from an account.
    Incoming transactions have a positive `amount` whereas outgoing have a negative one.
    """

    date = DateField()
    description = CharField(max_length=35)
    transaction_number = CharField(max_length=18, unique=True, db_index=False)
    amount = DecimalField(max_digits=6, decimal_places=2)
    category = ForeignKey(TransactionCategory, on_delete=SET_NULL, null=True)

    class Meta:
        db_table = "transactions"

    @classmethod
    def find_by_transaction_number(
        cls, transaction_number: str
    ) -> Optional["Transaction"]:
        """Find a model by transaction number. Returns None if the model is not found."""
        try:
            return cls.objects.get(transaction_number=transaction_number)
        except cls.DoesNotExist:
            return None
