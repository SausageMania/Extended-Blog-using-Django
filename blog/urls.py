from . import views
from django.urls import path

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('post/draft/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/remove', views.post_delete, name='post_delete'),
    path('post/signup/', views.signup, name='signup'),
    path('post/<int:pk>/comment/new', views.add_comment, name = 'add_comment'),
    path('post/<int:pk>/comment/approve/', views.comment_approve, name = 'comment_approve'),
    path('post/<int:pk>/comment/<int:cpk>/remove/', views.comment_remove, name='comment_remove'),
    path('post/<int:pk>/comment/<int:cpk>/edit', views.comment_edit, name='comment_edit'),
    path('post/<int:pk>/comment/<int:cpk>/',views.comment_detail, name='comment_detail'),
]