import uuid
from django.db import models


class RequestCounter(models.Model):
    count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'request_counter'


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Collection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    movies = models.ManyToManyField(Movie, related_name='collections')
    collection_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
