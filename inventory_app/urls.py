from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('create/', views.item_create, name='item_create'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('update/<int:pk>/', views.item_update, name='item_update'),
    path('delete/<int:pk>/', views.item_delete, name='item_delete'),
    path('borrow/<int:pk>/', views.borrow_item, name='borrow_item'),
    path('return/<int:pk>/', views.return_item, name='return_item'),
    path('my_borrows/', views.my_borrows, name='my_borrows'),
    # Maintenance URLs
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('item/<int:item_pk>/schedule_maintenance/', views.schedule_maintenance, name='schedule_maintenance'),
    path('maintenance/<int:pk>/update/', views.update_maintenance, name='update_maintenance'),
]
