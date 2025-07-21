from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register-user'),
    path('veri_user/', views.veri_user, name='verify-user'),
    path('register_admin/', views.register_admin, name='register-admin'),
    path('veri_admin/', views.veri_admin, name='verify-admin'),
    path('login_user/', views.login_user),
    path('login_admin/', views.login_admin),
    path('reset-password/', views.reset_password),
    path('pets/', views.pet_list_create, name='pet-list-create'),
    path('pets/<int:pk>/', views.pet_detail, name='pet-detail'),
    path('categories/', views.category_list_create),
    path('adopt/', views.apply_for_adoption),
    path('adopt/update-status/<int:pk>/', views.update_adoption_status),
    path('my-adoptions/', views.user_adoptions),
    path('all-adoptions/', views.all_adoptions)
 
    
]                                                                                                                                                                                       
