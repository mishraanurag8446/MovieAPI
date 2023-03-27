import os

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Collection, Movie
from .serializers import CollectionSerializer


# from .serializers import RegistrationSerializer, CollectionSerializer


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegistrationSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         refresh = RefreshToken.for_user(user)
#
#         response = {
#             "refresh": str(refresh),
#             "access": str(refresh.access_token)
#         }
#
#         return Response(response, status=status.HTTP_201_CREATED)
#

@api_view(['GET'])
def movies(request):
    # username = 'iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0'
    # password = 'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'

    username = os.getenv('USERNAME1')
    password = os.getenv('PASSWORD')
    url = 'https://demo.credy.in/api/v1/maya/movies/'

    # Create a session
    session = requests.Session()

    # Set the authentication credentials for the session
    session.auth = (username, password)

    # Make a request to the API
    response = session.get(url)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        movie = response.json()
        return Response(movie)
    # return Response(response.error)


class CollectionView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        collection_data = Collection.objects.all()
        data = CollectionSerializer(collection_data, many=True)
        return Response(data.data)

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        movie_list = request.data.get('movies')
        collection = Collection(title=title, description=description)
        collection.save()
        for movie in movie_list:
            title = movie.get('title')
            description = movie.get('description')
            genres = movie.get('genres')
            movie = Movie(title=title, description=description, genres=genres)
            movie.save()
        data = {'collection_uuid': collection.collection_uuid}
        return Response(data)

    def put(self, request, collection_id):
        data = request.data
        collection = Collection.objects.get(collection_uuid=collection_id)
        collection.title = request.data.get('title')
        collection.description = request.data.get('description')
        collection.save()
        print(request.data.get('movies'))
        for movie in request.data.get('movies'):
            title = movie.get('title')
            description = movie.get('description')
            genres = movie.get('genres')
            movie = Movie(title=title, description=description, genres=genres)
            movie.save()
            # collection.movies.add(movie)
        data = {'collection_uuid': collection.collection_uuid}
        return Response(data)

    def delete(self, request, collection_id):
        collection = Collection.objects.get(collection_uuid=collection_id)
        collection.delete()
        return Response()


@api_view(['GET'])
def total_requests(request):
    response_data = {'total_requests': request.META.get('X-Total-Requests', 'unknown')}
    return Response(response_data)


#
# @api_view(['GET', 'POST'])
# def movie(request):
#     if request.method == 'POST':
#         title = request.data.get('title')
#         description = request.data.get('description')
#         genres = request.data.get('genres')
#         print(request.data)
#         print(title, genres, description)
#         movie = Movie(title=title, description=description, genres=genres)
#         movie.save()
#         # movie_data = MovieSerializer(movie)
#         return Response({'UUID': movie.uuid})
#     if request.method == 'GET':
#         movie_list = Movie.objects.all()
#         # print(movie_list)
#         serialize_movie = MovieSerializer(movies, many=True)
#         # print(serialize_movie)
#         return Response(serialize_movie.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def movie_collection(request, collection_id=None):
    data = None
    if request.method == 'GET':
        collection_data = Collection.objects.all()
        data = CollectionSerializer(collection_data, many=True)
        return Response(data.data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        movie_list = request.data.get('movies')
        collection = Collection(title=title, description=description)
        collection.save()
        for movie in movie_list:
            title = movie.get('title')
            description = movie.get('description')
            genres = movie.get('genres')
            movie = Movie(title=title, description=description, genres=genres)
            movie.save()
        data = {'collection_uuid': collection.collection_uuid}
        return Response(data)
    elif request.method == 'PUT':
        data = request.data
        collection = Collection.objects.get(collection_uuid=collection_id)
        collection.title = request.data.get('title')
        collection.description = request.data.get('description')
        for movie in request.data.get('movies'):
            title = movie.get('title')
            description = movie.get('description')
            genres = movie.get('genres')
            movie = Movie(title=title, description=description, genres=genres)
            movie.save()
            collection.movies.add(movie)
    elif request.method == 'DELETE':
        collection = Collection.objects.get(collection_uuid=collection_id)
        collection.delete()
        return Response()
    return Response(data.error)


@api_view(['GET'])
def reset_count(request):
    response = {'message': 'request count reset successfully'}
    return Response(response)
