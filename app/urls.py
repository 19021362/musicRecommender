from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('getdata/', views.get_data, name='get_data'),
    path('sample/<int:sample_id>/', views.recommendation_detail, name='detail'),
    #path('<int:sample_id>/recommendation', views.recommendation_detail, name='recommendation_detail'),
    path('track/<str:id>/', views.choose_song, name='choose_song'),
    path('add/<str:id>/', views.add_song_playlist, name='add_song'),
    path('remove/<str:id>/', views.remove_song_playlist, name='remove_song'),
    path('search/<str:subname>/', views.search, name='search')
]