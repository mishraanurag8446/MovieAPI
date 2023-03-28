from .models import Collection, Movie
from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = '__all__'

    def update(self, instance, validated_data):
        # Update the Collection fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        # Update the nested Movie objects
        movies_data = validated_data.get('movies')
        if movies_data:
            for movie_data in movies_data:
                movie_uuid = movie_data.pop('uuid', None)
                try:
                    movie = instance.movies.get(uuid=movie_uuid)
                    movie.title = movie_data.get('title', movie.title)
                    movie.description = movie_data.get('description', movie.description)
                    movie.genres = movie_data.get('genres', movie.genres)
                    movie.save()
                except Movie.DoesNotExist:
                    pass

        instance.save()
        return instance
