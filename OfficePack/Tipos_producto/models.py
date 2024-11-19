import uuid
from django.db import models
from Producto.models import Producto
from django.utils.text import slugify
from django.db.models.signals import pre_save

class Tipo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    products = models.ManyToManyField(Producto, blank=True)
    created_at= models.DateTimeFiled(auto_now_add=True)
    slug = models.SlugField(null=False, blank=False, unique=True, default='')
    image = models.ImageField(upload_to='/tipos',null = True, blank=False)
    def __str__(self):
        return self.title
    
def set_slug(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)
        while Category.objects.filter(slug=slug).exists():
            slug = slugify("{}-{}".format(instance.title,str(uuid.uuid4())[:8]))
            print("Este es slug", slug)
        instance.slug = slug

pre_save.connect(set_slug, sender=Category)