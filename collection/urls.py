from django.urls import path
from .views import *

urlpatterns = [
    path('movies/', MovieListView.as_view(authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated]), name='movies'),
    path('collection/', CollectionView.as_view(authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated]), name='collections'),
    path('collection/<str:collection_id>/', CollectionView.as_view(authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated]), name='collections'),
    path('request-count/', RequestCountView.as_view(authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated]), name='request-count'),
    path('request-count/reset/', RequestCountView.as_view(authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated]), name="request-count-reset"),
]
