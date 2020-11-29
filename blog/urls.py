from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView
                    )
from . import views
urlpatterns = [
    path('',PostListView.as_view(),name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/',views.about,name='blog-about'),
    path('post_view_api/',views.PostGenericAPIView.as_view(),name='post_view_api'),
    path('post_detail_api/<int:pk>/',views.PostGenericDetailAPIView.as_view(),name='post-detail-api')

]
