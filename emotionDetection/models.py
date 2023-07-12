from django.db import models
from django.dispatch import receiver
import os


# Create your models here.
class UploadFile(models.Model):
    """
    Store file in folder
    """
    file = models.FileField(upload_to='audio/')


@receiver(models.signals.post_delete, sender=UploadFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
