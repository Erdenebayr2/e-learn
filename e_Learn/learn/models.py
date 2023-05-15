from django.db import models
from .validators import file_size

class Video(models.Model):
    Гарчиг = models.CharField(max_length=100)
    Бичлэг = models.FileField(upload_to="learn/%y", validators=[file_size])
    Тайлбар = models.CharField(max_length=300)
    def __str__(self):
        return self.caption