from django.db import models

from django.urls import reverse

from ckeditor.fields import RichTextField

from category.models import Category, Tag

from user.hashid import encode_id


class Product(models.Model):
    """
    Model representing a product in the inventory.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text='Name of the product.',
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
        help_text='URL-friendly identifier for the product.'
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        limit_choices_to={'category_type': Category.CategoryType.PRODUCT},
        db_index=True,
        help_text='Category to which the product belongs.',
        related_name='products_category',
    )
    tags = models.ManyToManyField(
        to=Tag,
        blank=True,
        help_text='Tags associated with the product.',
        related_name='products_tags',
    )
    image = models.ImageField(
        upload_to='products/images/',
        null=True,
        blank=True,
        help_text='Image representing the product.'
    )
    description = RichTextField(
        blank=True,
        null=True,
        help_text='Detailed description of the product.'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text='Price of the product.'
    )
    percentage = models.PositiveIntegerField(
        default=0,
        help_text='Discount percentage for the product.'
    )
    availability = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Availability status of the product (e.g., In Stock, Out of Stock).'
    )
    shipping_details = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Shipping information for the product.'
    )
    weight = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='Weight of the product.'
    )
    stock = models.PositiveIntegerField(
        help_text='Available stock quantity.',
        default=1,
    )  # Stock must be at least 1
    is_available = models.BooleanField(
        default=True,
        help_text='Availability status of the product.'
    )
    views_count = models.PositiveIntegerField(default=0, help_text="Views count: ")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text='Timestamp when the product was created.')
    updated_at = models.DateTimeField(
        auto_now=True, help_text='Timestamp when the product was last updated.')

    def __str__(self):
        return f"{self.pk} - {self.name}"

    class Meta:
        ordering = ['name']  # Default ordering by product name
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['name'], name='product_name_idx'),
            models.Index(fields=['slug'], name='product_slug_idx'),
            models.Index(fields=['category'], name='product_category_idx'),
        ]

    def discounted_price(self):
        """
        Calculate the price after applying the discount percentage.
        """
        if self.percentage > 0:
            discount_amount = (self.percentage / 100) * self.price
            return self.price - discount_amount
        return self.price

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = encode_id(self.pk)
    #     super().save(*args, **kwargs)
