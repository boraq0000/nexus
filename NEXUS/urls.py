"""
URL configuration for NEXUS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('nexus-admin-2026/', admin.site.urls),
    path('api/login/', views.login_check, name='login_check'),
    path('api/logout/', views.logout_view, name='logout_view'),
    path('api/current-user/', views.current_user, name='current_user'),
    path('api/signup/', views.signup_check, name='signup_check'),
    path('api/users/', views.get_users_by_role, name='get_users_by_role'),
    path('api/projects/', views.projects_list, name='projects_list'),
    path('api/projects/create/', views.create_project, name='create_project'),
    path('api/my-projects/', views.my_projects, name='my_projects'),
    path('api/projects/<int:project_id>/apply/', views.apply_project, name='apply_project'),
    path('api/projects/<int:project_id>/members/', views.get_project_members, name='get_project_members'),
    path('api/projects/<int:project_id>/grades/', views.get_project_grades, name='get_project_grades'),
    path('api/projects/<int:project_id>/respond-invite/', views.respond_invite, name='respond_invite'),
    path('api/professor-projects/', views.professor_projects, name='professor_projects'),
    path('api/projects/<int:project_id>/approve/', views.approve_project, name='approve_project'),
    path('api/projects/grade/', views.grade_project, name='grade_project'),
    path('api/invest/', views.invest_project, name='invest_project'),
    path('api/rate/', views.rate_project, name='rate_project'),
]
