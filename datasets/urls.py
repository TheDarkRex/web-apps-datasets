from django.urls import path
from . import views

app_name = 'datasets'

urlpatterns = [
    path('', views.DatasetListView.as_view(), name='list'),
    path('register/', views.SignUpView.as_view(), name='signup'),
    path('create/', views.DatasetCreateView.as_view(), name='create'),
    path('<int:pk>/', views.DatasetDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.DatasetUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DatasetDeleteView.as_view(), name='delete'),
    path('<int:query_pk>/answer/', views.AnswerCreateView.as_view(), name='add_answer'),
    path('<int:dataset_pk>/query/', views.QueryCreateView.as_view(), name='add_query'),
    path('query/<int:pk>/delete/', views.QueryDeleteView.as_view(), name='delete_query'),
    path('answer/<int:pk>/delete/', views.AnswerDeleteView.as_view(), name='delete_answer'),
    path('<int:dataset_pk>/schemat/', views.SchemaUpdateView.as_view(), name='schema_update'),
]