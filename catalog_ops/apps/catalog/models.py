from django.db import models
from uuid import uuid4

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(BaseModel):
    uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )
    name = models.CharField(
        default="Product name",
        max_length=150,
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class ProductsCollection(BaseModel):

    uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )
    name = models.CharField(
        default="Collection name",
        max_length=150,
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name="products",
    )
    description = models.TextField(blank=True)
