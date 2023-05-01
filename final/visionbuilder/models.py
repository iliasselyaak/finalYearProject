from django.db import models
from django.contrib.auth.models import User

# Page model.

class Page(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    content = models.JSONField(default=dict) # JSONField containing all of the editor's components.
    public = models.BooleanField(default=False) # Whether or not the page is public.
    html = models.TextField(default="") # HTML code for the page.
    css = models.TextField(default="") # CSS code for the page.

    def __str__(self):
        return f"{self.user.username} - {self.name}" # String representation of the page.
