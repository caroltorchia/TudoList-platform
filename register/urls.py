from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="signup"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # path("<int:question_id>/", views.detail, name="detail"),
   
    # path("<int:question_id>/results/", views.results, name="results"),
    
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]