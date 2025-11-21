from django.db import models

from ckeditor.fields import RichTextField

from category.models import Category, Tag
from user.models import CustomUser

from django.urls import reverse
from django.utils.text import slugify

import uuid
import datetime


class Article(models.Model):
    name = models.CharField(
        max_length=255,
        help_text="The name of the article.",
        unique=True,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
        help_text="A URL-friendly slug for the article.",
    )
    image = models.ImageField(
        upload_to='articles/images/',
        help_text="An image representing the article.",
        null=True,
        blank=True,
    )
    description = RichTextField(help_text="A detailed description of the article.", null=True, blank=True)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        limit_choices_to={'category_type': Category.CategoryType.ARTICLE},
        db_index=True,
        help_text="The category to which this article belongs.",
        related_name='articles',
    )
    tags = models.ManyToManyField(
        to=Tag,
        blank=True,
        help_text="Tags associated with this article.",
        related_name='articles_tags',
    )
    author = models.ForeignKey(
        to=CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The author of the article.",
        related_name='articles_author',
        db_index=True,
    )
    views_count = models.PositiveIntegerField(
        default=0,
        help_text="The number of times the article has been viewed.",
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="The time when the article was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The time when the article was last updated.")

    def __str__(self):
        return f"{self.id} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            date_slug = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            uuid_slug = uuid.uuid4().hex[:8]
            self.slug = f"{base_slug}-{date_slug}-{uuid_slug}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        indexes = [
            models.Index(fields=['name'], name='article_name_idx'),
            models.Index(fields=['slug'], name='article_slug_idx'),
            models.Index(fields=['category'], name='category_article_idx'),
            models.Index(fields=['author'], name='author_article_idx'),
        ]
        ordering = ['-created_at']
