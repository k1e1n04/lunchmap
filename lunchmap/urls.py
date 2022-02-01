from django.urls import path
from . import views

app_name = 'lunchmap'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('review_create', views.review_create, name='review_create'),
    path('<int:id>/review_delete', views.review_delete, name='review_delete'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
]