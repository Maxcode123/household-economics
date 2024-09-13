from typing import Self, Optional

from django.db.models import Model, DateTimeField
from django.contrib import admin


def register_admin(model_cls):
    admin.site.register(model_cls)
    return model_cls


class BaseModel(Model):
    class Meta:
        abstract = True

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        d = vars(self)
        d.pop("_state", None)
        return str(d)

    @classmethod
    def find(cls, id: int) -> Optional[Self]:
        """Find a model by id. Returns None if the model is not found."""
        try:
            return cls.objects.get(id=id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def all(cls, *, descending: bool = True) -> list[Self]:
        """Return all objects sorted by id."""
        field = "id" if descending else "-id"

        return cls.objects.order_by(field).all()

    @classmethod
    def count(cls) -> int:
        """Returns the number of records currently in DB."""
        return cls.objects.count()
