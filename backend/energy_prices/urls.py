from django.urls import path

from . import views

app_name = 'energy_price_api'

urlpatterns = [

    path('', views.ListEnergyPrice.as_view(), name="energy_price_list"),
    # path('<int:pk>/', views.DetailTodo.as_view(), name="todo_detail"),
]