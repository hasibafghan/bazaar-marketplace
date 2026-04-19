from django.db import models
from django.urls import reverse
from category.models import Category
from accounts.models import Account
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

class Product(TranslatableModel):
    translations = TranslatedFields(
        product_name=models.CharField(max_length=200),
        description=models.TextField(max_length=500, blank=True),
    )
    slug            = models.SlugField(max_length=200, unique=True)  # Non-translatable for URL
    price           = models.IntegerField()
    old_price       = models.IntegerField()
    images          = models.ImageField(upload_to='products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail' , args=[self.category.slug , self.slug])

    def __str__(self):
        return self.product_name
    
    # calculate average review stars
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

#  ==========================| variation model |===============================


variation_category_choice = (
    ('color', _('Color')),  # also fix: translate the labels
    ('size',  _('Size')),
)

class Variation(TranslatableModel):
    translations = TranslatedFields(
        variation_value=models.CharField(max_length=100),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            return self.variation_value  # safe with try/except
        except Exception:
            return f"Variation {self.pk}"
    

class ReviewRating(TranslatableModel):
    translations = TranslatedFields(
        subject=models.CharField(max_length=100, blank=True),
        review=models.TextField(max_length=500, blank=True),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userporfile = models.OneToOneField('accounts.UserProfile', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models. ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name
    class Meta:
        verbose_name = 'product gallery'
        verbose_name_plural = 'product gallery'