from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=100)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name
    
def get_image_field(instance, filename):
    name = instance.author.username
    slug = slugify(name)
    return f"posts/{slug}-{filename}"
    
class Post(models.Model):
    title = models.CharField(_("Post title"), max_length=250)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name="posts",
        null = True,
        on_delete= models.SET_NULL,
    )
    image = models.ImageField(upload_to=get_image_field, blank=True)
    categories = models.ManyToManyField(Category, related_name="post_lists", blank=True)
    body =  models.TextField(_("Post body"))
    
    #each post can be liked by multiple users and vice versa
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="post_likes", blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True) # will work when instances is created
    updated_at = models.DateTimeField(auto_now=True) # will work when the instance is saved
    
    class Meta:
        ordering = ("-created_at",)
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name= "post_comments",
        null = True,
        on_delete= models.SET_NULL
    )
    
    body = models.TextField(_("Comments body"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ("-created_at",)
    
    def __str__(self):
        return f"{self.body[:20]} by {self.author.username}"