import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True, blank=True, max_length=80)
    description = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)
    user_id = models.ManyToManyField(User, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Change save for adding auto slug.
        """
        self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)

    def short_description(self):
        """
        Short description for product.
        """
        if len(self.description) < 250:
            return self.description
        return self.description[:250] + '...'

    def change_state_like(self, user_id):
        """
        Change like. Parameter user_id is for save "one user - one like"
        """
        liked = self.user_id.filter(id=user_id)
        if not liked.exists():
            self.like_count += 1
            self.user_id.add(user_id)
        else:
            self.like_count -= 1
            self.user_id.remove(user_id)
        self.save()


class CommentQuerySet(models.QuerySet):
    def recently_added(self, product):
        # query = self.raw('''Select * from product_comment
        #               WHERE product_id_id=%s AND created_at > now() - interval 1 day
        #               ORDER BY -created_at;''', [product.id])
        difference = timezone.now() - datetime.timedelta(hours=24)
        query = self.filter(product_id=product).filter(created_at__gt=difference).order_by('-created_at')
        return query

    def add_comment(self, comment_text, product):
        comment = self.create(text=comment_text, product_id=product)
        return comment


class Comment(models.Model):
    text = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    product_id = models.ForeignKey(Product)

    objects = CommentQuerySet.as_manager()

    def __str__(self):
        return '{0}  --  {1}'.format(self.text, self.product_id.name)
