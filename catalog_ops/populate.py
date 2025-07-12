import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catalog_ops.settings")
django.setup()

from apps.catalog.factories import ProductFactory, ProductsCollectionFactory

def run():
    
    print("Creating collections...")
    for _ in range(10):
        products = ProductFactory.create_batch(5)
        ProductsCollectionFactory(products=products)

    print("Done.")

if __name__ == "__main__":
    run()