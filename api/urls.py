from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register-user'),
    path('register-admin/', views.register_admin, name='register-admin'),
    path('pets/', views.pet_list_create, name='pet-list-create'),
    path('pets/<int:pk>/', views.pet_detail, name='pet-detail'),
    path('categories/', views.category_list_create),
    path('adopt/', views.apply_for_adoption),
   path('adopt/update-status/<int:pk>/', views.update_adoption_status),
   path('my-adoptions/', views.user_adoptions),
    path('all-adoptions/', views.all_adoptions)
    
    
    
]                                                                                                                                                                                       
