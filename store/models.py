from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# this class extends from default model manager
class ProductManager(models.Manager):
    def get_queryset(self):
        # here we returning a different quey set
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    # ADDING PLURAL NAME TO CATEGORY
    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    # category of a product. Related to category table.
    # If category is deleted all products are deleted too
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    # creator of a product entry
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')
    # title of the book
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    # image of a product. It is here because it s simple application
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    # might be some products that are not active to buy
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # objects is a default model manager
    objects = models.Manager()
    # product is custom manager
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title
