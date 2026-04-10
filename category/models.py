from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(
        category_name=models.CharField(max_length=50),
        description=models.TextField(max_length=255, blank=True),
    )
    slug            = models.SlugField(max_length=100, unique=True)  # Non-translatable for URL
    category_image  = models.ImageField(upload_to='category', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name