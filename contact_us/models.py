from django.db import models
from ckeditor.fields import RichTextField


class ContactMessage(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Full name of the person contacting.",
    )
    email = models.EmailField(
        max_length=254,
        help_text="Email address of the person contacting.",
    )
    message = RichTextField(
        help_text="The message content from the contact form.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the message was created.",
    )

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        # ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} <{self.email}>"
