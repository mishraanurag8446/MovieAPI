from django.urls import path
from .views import *

urlpatterns = [
    path('movies/', movies, name='movies'),
    path('collection/', CollectionView.as_view(authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated]), name='collections'),
    path('collection/<str:collection_id>/', CollectionView.as_view(), name='collections'),
    path('request-count/', RequestCountView.as_view(), name='request-count'),
    path('request-count/reset/', RequestCountView.as_view(), name="request-count-reset"),
]
