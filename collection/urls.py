from django.urls import path
from .views import *

urlpatterns = [
    # path('token/', ObtainTokenView.as_view(), name='token_obtain_pair'),

    # path('register/', RegisterView.as_view(), name='Register'),
    path('movies/', movies, name='Movies'),
    path('collection/', CollectionView.as_view(), name='Collections'),
    path('collection/<str:collection_id>/', CollectionView.as_view(), name='Collections'),
    path('request-count/', total_requests),
    path('request-count/reset/', reset_count),
]
