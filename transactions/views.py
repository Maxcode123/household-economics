from django.shortcuts import render
from django.http import HttpRequest

from transactions.models import Transaction


def index_transaction_view(request: HttpRequest):
    """GET /transactions/"""
    return render(
        request,
        "transactions/index.html",
        context={"transactions": Transaction.all(descending=True)},
    )
