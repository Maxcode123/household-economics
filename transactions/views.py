from django.shortcuts import render
from django.http import HttpRequest

from transactions.models import Transaction, TransactionCategory


def index_transaction_view(request: HttpRequest):
    """GET /transactions/"""
    return render(
        request,
        "transactions/index.html",
        context={"transactions": Transaction.all(descending=True)},
    )


def index_transaction_categories_view(request: HttpRequest):
    """GET /transactions/categories"""
    return render(
        request,
        "transactions/categories/index.html",
        context={"categories": TransactionCategory.all(descending=True)},
    )
