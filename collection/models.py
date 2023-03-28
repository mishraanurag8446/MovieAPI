import uuid
from django.db import models


class RequestCounter(models.Model):
    # id = models.IntegerField(primary_key=True, auto_now_add=True)
    count = models.PositiveIntegerField(default=0)

    # date = models.DateField(primary_key=True)

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

# class RequestCounter(models.Model):
#     id = models.DateTimeField(primary_key=True, auto_now_add=True)
#     date = models.DateField(default=now)
#     count = models.IntegerField(default=0)
