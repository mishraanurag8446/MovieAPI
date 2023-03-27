from django.db import models
import uuid

# Create your models here.


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


class RequestCounter(models.Model):
    date = models.DateField(primary_key=True)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'request_counter'

# class RequestCount(models.Model):
