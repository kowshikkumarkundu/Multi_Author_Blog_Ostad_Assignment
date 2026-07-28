from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.author_dashboard, name='author_dashboard'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<slug:slug>/like/', views.toggle_like, name='toggle_like'),
    path('author/<str:username>/', views.author_profile, name='author_profile'),
]