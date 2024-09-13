from django.urls import path

from transactions.views import index_transaction_view, index_transaction_categories_view

urlpatterns = [
    path("", index_transaction_view, name="index-transactions-view"),
    path(
        "categories/",
        index_transaction_categories_view,
        name="index-transaction-categories-view",
    ),
]
