from django.db import models
from django.utils.translation import gettext_lazy as _

class ImageModel(models.Model):
    # Field to store a title or description of the image
    title = models.CharField(max_length=100, blank=True, null=True)

    # Field to store the image
    image = models.ImageField(
        upload_to='images/',  # Directory within the media root to store the images
        blank=False,          # This field is required
        null=False            # Cannot be null in the database
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    sift = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name