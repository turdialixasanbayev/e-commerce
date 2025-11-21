from django.db import models

from user.models import CustomUser


class WishList(models.Model):
    user = models.OneToOneField(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='wishlists',
        db_index=True,
        help_text='The user who owns this wishlist item.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='The date and time when the wishlist was created.',
    )

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user'], name='user_wishlist_idx'),
        ]

    def __str__(self):
        return f"WishList of ({self.user})"


class WishListItem(models.Model):
    wishlist = models.ForeignKey(
        to=WishList, on_delete=models.CASCADE, related_name="wishlist_items", db_index=True, help_text='The wishlist to which this item belongs.')
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name='wishlist_product_items', db_index=True, help_text='The product added to the wishlist.')
    created_at = models.DateTimeField(
        auto_now_add=True, help_text='The date and time when the wishlist item was added.')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['wishlist', 'product'],
                name='unique_wishlist_product'
            ),
        ]
        verbose_name = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['wishlist'], name='wishlist_item_wishlist_idx'),
            models.Index(fields=['product'], name='wishlist_item_product_idx'),
        ]

    def __str__(self):
            return f"{self.id} - {self.product.name}"
