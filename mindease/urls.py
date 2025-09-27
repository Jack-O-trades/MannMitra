from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main Pages
    path('', views.home, name='home'),
    path('alogin/', views.alogin, name='alogin'),
    path('slogin/', views.slogin, name='slogin'),
    path('about/', views.about, name='about'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('counselors/', views.counselors, name='counselors'),
    path('community/', views.community, name='community'),
    path('resources/', views.resources, name='resources'),
    path('contact/', views.contact, name='contact'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('signup/', views.signup, name='signup'),
    path('booking/', views.booking, name='booking'),
    path('career/', views.career_resources, name='career_resources'),
    path('screening/', views.screening, name='screening'),

    # Admin Dashboard
    path("admin-dashboard/", views.adashboard, name="admin_dashboard"),

    # Institution Dashboard
    path("institution-dashboard/", views.inst_dashboard, name="inst_dashboard"),
    path('institution/content/', views.inst_content, name='inst_content'),
    path('institution/doctor/', views.doctor_institution, name='doctor_institution'),
    path('institution/analytics/', views.inst_analytics, name='inst_analytics'),
    path('institution/student/', views.inst_student, name='inst_student'),
    path('institution/counselors/', views.inst_counselors, name='inst_counselors'),
    path('institution/alert/', views.inst_alert, name='inst_alert'),

    # Student Dashboard
    path("student/stu_dashboard", views.stu_dashboard, name="stu_dashboard"),
    path('studentdashboard/myprogress/', views.stu_progress, name='stu_progress'),
    path('studentdashboard/resource/', views.stu_resource, name='stu_resource'),
    path("auth/callback/", views.auth_callback, name="auth_callback"),

]
