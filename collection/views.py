import os
import requests
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Collection, Movie
from .models import RequestCounter
from .serializers import CollectionSerializer, MovieSerializer


class RequestCountView(APIView):

    def get(self, request):
        # Create a new request counter instance
        request_counter = RequestCounter.objects.get(id=1)
        # Return the new request counter ID and count as a JSON response
        response_data = {
            'count': request_counter.count,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def post(self, request):
        # Delete the request counter instance with the given ID
        try:
            request_counter = RequestCounter.objects.get(id=1)
            request_counter.count = 0
            request_counter.save()
            return Response({'message': 'Request counter reset successfully'})
        except RequestCounter.DoesNotExist:
            return Response({'message': False, 'message': 'failed to reset count'},
                            status=status.HTTP_404_NOT_FOUND)


class CollectionView(APIView):
    # authentication_classes = [SessionAuthentication, TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        collection_data = Collection.objects.all()
        data = CollectionSerializer(collection_data, many=True)
        return Response(data.data)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            # Create a new Collection object
            collection = Collection.objects.create(
                title=serializer.validated_data['title'],
                description=serializer.validated_data['description']
            )
            # Add movies to the collection
            print(serializer.validated_data)
            for movie_data in serializer.validated_data['movies']:
                movie, created = Movie.objects.get_or_create(
                    title=movie_data['title'],
                    description=movie_data['description'],
                    genres=movie_data['genres'],
                    # uuid=movie_data['uuid']
                )
                collection.movies.add(movie)

            # Serialize the Collection object and return it in the response
            response_data = {
                'collection_uuid': str(collection.collection_uuid)
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, collection_id):

        collection = Collection.objects.get(collection_uuid=collection_id)
        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, collection_id):
        try:
            collection = Collection.objects.get(collection_uuid=collection_id)
            collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Collection.DoesNotExist:
            # If the collection doesn't exist, return a 404 response
            return Response({'message': f'Collection with ID {collection_id} does not exist'},
                            status=status.HTTP_404_NOT_FOUND)


class MovieListView(APIView):
    pagination_class = PageNumberPagination
    page_size = 5

    def get(self, request):
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        url = 'https://demo.credy.in/api/v1/maya/movies/'

        try:
            # Create a session
            session = requests.Session()
            session.auth = (username, password)
            response = session.get(url)

            movies = response.json()
            return Response(movies)
        except requests.exceptions.ConnectionError as e:
            # Handles connection errors
            return Response({'message': f'Connection Error: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.Timeout as e:
            # Handles timeout errors
            return Response({'message': f'Timeout Error: {e}'}, status=status.HTTP_408_REQUEST_TIMEOUT)
