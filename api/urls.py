from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('users/', views.UserListView.as_view()),
    path('users/<str:pk>', views.UserDetailsView.as_view()),
    path('notification/', views.NotificationView.as_view()),
    path('notification/<str:pk>', views.NotificationDetailView.as_view()),
    path('notification/statistics', views.NotificationListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)