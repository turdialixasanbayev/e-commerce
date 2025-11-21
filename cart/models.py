from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        to='user.CustomUser',
        on_delete=models.CASCADE,
        related_name='carts',
        db_index=True,
        help_text="The user who owns this cart."
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The time the cart was created.")

    def __str__(self):
        return f"Cart of {self.user}"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user'], name='user_cart_idx'),
        ]


class CartItem(models.Model):
    cart = models.ForeignKey(
        to=Cart,
        on_delete=models.CASCADE,
        related_name='items',
        db_index=True,
        help_text="The cart to which this item belongs.",
    )
    product = models.ForeignKey(
        to='product.Product',
        on_delete=models.CASCADE,
        related_name='cart_items',
        db_index=True,
        help_text="The product added to the cart."
    )
    quantity = models.PositiveIntegerField(
        default=1, help_text="The quantity of the product in the cart.")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The time the item was added to the cart.")

    def __str__(self):
        return f"{self.quantity} of {self.product} in {self.cart}"

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('cart', 'product')
        indexes = [
            models.Index(fields=['cart'], name='cart_item_idx'),
            models.Index(fields=['product'], name='product_item_idx'),
        ]
