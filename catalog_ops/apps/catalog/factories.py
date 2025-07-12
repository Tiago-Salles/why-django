import factory
from faker import Faker
from .models import Product, ProductsCollection

fake = Faker()

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    uuid = factory.Faker("uuid4")
    name = factory.Faker("word")
    price = factory.LazyFunction(lambda: round(fake.pydecimal(left_digits=4, right_digits=2, positive=True, max_value=250, min_value=3), 2))
    is_active = factory.Faker("boolean")
    quantity = factory.Faker("random_int", min=0, max=1000)
    description = factory.Faker("paragraph")

class ProductsCollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductsCollection

    name = factory.Faker("word")
    description = factory.Faker("sentence")

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.products.add(product)
        else:
            products = ProductFactory.create_batch(3)
            for product in products:
                self.products.add(product)