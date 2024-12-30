from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('exam/list/', views.exam_list, name='exam_list'),
    path('exam/take/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('exam/result/<int:exam_id>/', views.exam_result, name='exam_result'),
]
