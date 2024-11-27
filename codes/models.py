from django.db import models
from django.contrib.auth.models import User
from .utils import fetch_http_dog_data


class ResponseCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    image_jpg = models.URLField(blank=True, null=True)
    image_webp = models.URLField(blank=True, null=True)

    def fetch_data(self):
        """
        Fetch details for this response code from the https://http.dog API.
        """
        data = fetch_http_dog_data(self.code)
        if data:
            self.description = data.get("title", "")
            images = data.get("image", {})
            self.image_jpg = images.get("jpg", "")
            self.image_webp = images.get("webp", "")
            self.save()

    def __str__(self):
        return f"{self.code}: {self.description}"


class SavedList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    codes = models.JSONField(default=list)  # Set default as an empty list

    def __str__(self):
        return self.name
