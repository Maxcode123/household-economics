from django.urls import path

from transactions.views import index_transaction_view

urlpatterns = [path("", index_transaction_view, name="index-transactions-view")]
