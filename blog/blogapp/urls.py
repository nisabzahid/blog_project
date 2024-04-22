from django.urls import path
from . import views

app_name = 'blogapp'

urlpatterns = [
 # post views
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('<int:post_id>/post_comment/', views.post_comment,name='post_comment'),
]