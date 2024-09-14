from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.forms import Form, ChoiceField

from transactions.models import Transaction, TransactionCategory
from transactions.domain_models import TransactionCategoryEnum


def index_transaction_view(request: HttpRequest):
    """GET /transactions/"""
    return render(
        request,
        "transactions/index.html",
        context={"transactions": Transaction.all(descending=True)},
    )


class UpdateTransactionCategoryForm(Form):
    category_id = ChoiceField(
        label="Άλλαξε κατηγορία σε",
        choices=[(t.id, t.name) for t in TransactionCategoryEnum],
    )


def update_transaction_category_view(request: HttpRequest, transaction_id: int):
    """GET /transactions/<int:transaction_id>/update/"""
    transaction = Transaction.find(transaction_id)

    if transaction is None:
        return redirect("index-transactions-view")

    context = {"form": UpdateTransactionCategoryForm(), "transaction": transaction}
    return render(request, "transactions/update_form.html", context)


def update_transaction_category(request: HttpRequest, transaction_id: int):
    """POST /transactions/<int:transaction_id>/"""
    transaction = Transaction.find(transaction_id)

    if transaction is None:
        return redirect("index-transactions-view")

    category_id = request.POST["category_id"]

    if TransactionCategory.find(category_id) is None:
        return redirect("index-transactions-view")

    transaction.category_id = category_id
    transaction.save()
    return redirect("index-transactions-view")


def index_transaction_categories_view(request: HttpRequest):
    """GET /transactions/categories/"""
    return render(
        request,
        "transactions/categories/index.html",
        context={"categories": TransactionCategory.all(descending=True)},
    )


def add_transaction_category_view(request: HttpRequest): ...
