from django.db import models
from ckeditor.fields import RichTextField


class SubEmail(models.Model):
    """
    Model to store subscribed email addresses.
    """

    email = models.EmailField(max_length=150, null=True, blank=True, unique=True, db_index=True, help_text="Enter your email to subscribe")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the email was subscribed")

    def __str__(self):
        return f"Subscribed Email: {self.email}"

    class Meta:
        verbose_name = "Subscribed Email"
        verbose_name_plural = "Subscribed Emails"
        ordering = ['id']
        indexes = [models.Index(fields=['email'])]


class Banner(models.Model):
    """
    Model to store banner images for the website.
    """

    name = models.CharField(max_length=225, help_text="Name of the banner", unique=True, db_index=True)
    image = models.ImageField(upload_to='banners/', help_text="Upload banner image", null=True, blank=True)
    description = RichTextField(help_text="Description of the banner", null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', help_text="Parent banner if applicable", limit_choices_to={'parent__isnull': True})
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the banner was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time when the banner was last updated")

    def __str__(self):
        return f"Banner: {self.name}"

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['id']
        indexes = [models.Index(fields=['name'])]
