from django.db import models
from ckeditor.fields import RichTextField


class Order(models.Model):
    STATUS = (
        ('new', 'New'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        'user.CustomUser', on_delete=models.CASCADE, related_name='order_user', db_index=True, help_text='The user who placed the order')
    status = models.CharField(max_length=20, choices=STATUS,
                              default='new', help_text='Current status of the order')
    first_name = models.CharField(
        max_length=100, db_index=True, help_text='First name of the person who placed the order')
    last_name = models.CharField(
        max_length=100, db_index=True, help_text='Last name of the person who placed the order')
    email = models.EmailField(
        max_length=100, db_index=True, help_text='Contact email for the order')
    phone_number = models.CharField(
        max_length=20, db_index=True, help_text='Contact phone number for the order')
    address = models.CharField(
        max_length=255, help_text='Shipping address for the order')
    notes = RichTextField(
        blank=True, null=True, help_text='Additional notes or instructions for the order')
    created_at = models.DateTimeField(
        auto_now_add=True, help_text='The date and time when the order was created')
    updated_at = models.DateTimeField(
        auto_now=True, help_text='The date and time when the order was last updated')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        return f"Order {self.id} - {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_item_order', db_index=True, help_text='The order to which this item belongs')
    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, related_name='order_item_product', help_text='The product included in this order item', db_index=True)
    quantity = models.PositiveIntegerField(default=1, help_text='The quantity of the product ordered')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='The price of the product at the time of order')
    created_at = models.DateTimeField(
        auto_now_add=True, help_text='The date and time when the order item was created')
    updated_at = models.DateTimeField(
        auto_now=True, help_text='The date and time when the order item was last updated')

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.price})"
