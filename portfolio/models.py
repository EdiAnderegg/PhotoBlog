from django.db import models


class Collection(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="collections/")
    is_published = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class Photo(models.Model):
    collection = models.ForeignKey(
        Collection, related_name="photos", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="photos/")
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    capture_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    is_published = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.title or f"Photo {self.pk}"

    def _published_siblings(self):
        return Photo.objects.filter(collection=self.collection, is_published=True)

    def get_next_published(self):
        return (
            self._published_siblings()
            .filter(
                models.Q(display_order__gt=self.display_order)
                | models.Q(display_order=self.display_order, id__gt=self.id)
            )
            .order_by("display_order", "id")
            .first()
        )

    def get_previous_published(self):
        return (
            self._published_siblings()
            .filter(
                models.Q(display_order__lt=self.display_order)
                | models.Q(display_order=self.display_order, id__lt=self.id)
            )
            .order_by("-display_order", "-id")
            .first()
        )


class Photographer(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    portrait = models.ImageField(blank=True)
    instagram_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    hero_background = models.ImageField(blank=True)
    hero_foreground_object = models.ImageField(blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
