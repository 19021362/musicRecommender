from django.urls import path, re_path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    #path('getdata/', views.get_data, name='get_data'),
    path('<int:sample_id>/', views.sample_detail, name='sample_detail'),
    path('<int:sample_id>/recommendation', views.recommendation_detail, name='recommendation_detail'),
    path('<int:sample_id>/<str:id>', views.choose_song, name='choose_song')
]