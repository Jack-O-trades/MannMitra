from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def alogin(request):
    return render(request, 'inadlogin.html')

def slogin(request):
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def chatbot(request):
    return render(request, 'chatbot.html')

def counselors(request):
    return render(request, 'counselors.html')

def community(request):
    return render(request, 'community.html')

def resources(request):
    return render(request, 'resource.html')

def contact(request):
    return render(request, 'contact.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def signup(request):
    return render(request, 'signup.html')

def login_view(request):
    return render(request, "login.html")
    
def booking(request):
    return render(request, 'booking.html')

def screening(request):
    return render(request, 'screening.html')

# Admin Dashboard View (FIX ADDED HERE)
def adashboard(request):
    return render(request, 'AdminDashboard/adashboard.html')

# Institution Dashboard Views
def inst_dashboard(request):
    return render(request, 'InstDashboard/dashboard.html')

def inst_analytics(request):
    return render(request, 'InstDashboard/analytics.html')

def inst_student(request):
    return render(request, 'InstDashboard/student.html')

def inst_counselors(request):
    return render(request, 'InstDashboard/counselors.html')

def doctor_institution(request):
    return render(request, 'InstDashboard/doctor.html')

def inst_content(request):
    return render(request, 'InstDashboard/content.html')

def inst_alert(request):
    return render(request, 'InstDashboard/alert.html')

# Student Dashboard Views
def stu_progress(request):
    return render(request, 'Myprogress.html')

def stu_dashboard(request):
    return render(request, 'StudentDashboard/sdashboard.html')

def stu_resource(request):
    return render(request, 'StudentDashboard/resourcestu.html')

def career_resources(request):
    return render(request, 'career_resources.html')

# core/views.py
from django.shortcuts import redirect

def auth_callback(request):
    return redirect('stu_dashboard')  # Django URL name for student dashboard

