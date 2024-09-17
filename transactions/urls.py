from django.urls import path

from transactions.views import (
    index_transaction_view,
    index_transaction_categories_view,
    update_transaction_category,
    update_transaction_category_view,
    index_monthly_transaction_categories_view,
)

urlpatterns = [
    path("", index_transaction_view, name="index-transactions-view"),
    path(
        "<int:transaction_id>/update/",
        update_transaction_category_view,
        name="update-transaction-category-view",
    ),
    path(
        "<int:transaction_id>",
        update_transaction_category,
        name="update-transaction-category-endpoint",
    ),
    path(
        "categories/",
        index_transaction_categories_view,
        name="index-transaction-categories-view",
    ),
    path(
        "monthly/",
        index_monthly_transaction_categories_view,
        name="index-monthly-transactions-view",
    ),
]
