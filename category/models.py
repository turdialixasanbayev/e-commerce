from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid
from django.utils import timezone
from ckeditor.fields import RichTextField


class Tag(models.Model):
    name = models.CharField(max_length=225, db_index=True, unique=True, help_text="Tag name")
    slug = models.SlugField(max_length=225, unique=True, db_index=True, null=True, blank=True, help_text="Tag slug for URL")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the tag was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the tag was last updated")

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        indexes = [
            models.Index(fields=['name'], name='tag_name_idx'),
            models.Index(fields=['slug'], name='tag_slug_idx'),
        ]
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    """
    Category model for article and product
    """

    class CategoryType(models.TextChoices):
        PRODUCT = 'product', 'Product'
        ARTICLE = 'article', 'Article'

    name = models.CharField(max_length=225, db_index=True, unique=True, help_text="Category name")
    slug = models.SlugField(max_length=225, unique=True, db_index=True, null=True, blank=True, help_text="Category slug for URL")
    category_type = models.CharField(
        max_length=50,
        choices=CategoryType.choices,
        default=None,
        null=True,
        blank=True,
        help_text="Select category type"
    )
    image = models.ImageField(upload_to='categories/', null=True, blank=True, help_text="Image representing the category")
    description = RichTextField(null=True, blank=True, help_text="Description of the category")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the category was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the category was last updated")

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['name'], name='category_name_idx'),
            models.Index(fields=['slug'], name='category_slug_idx'),
        ]
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            date_slug = timezone.now().strftime("%Y%m%d")
            uuid_slug = uuid.uuid4().hex[:8]
            self.slug = f"{base_slug}-{date_slug}-{uuid_slug}"
        super().save(*args, **kwargs)
