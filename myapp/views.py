

from django.core.mail import send_mail
from django.conf import settings

from .models import PricingPlan
from .models import ConsultationRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import ContactMessage, CustomUser, TeamMember, Service, Feedback
# from .models import PricingPlan
# --- Static Home Page
def home(request):
    return HttpResponse("This is the dashboard (home) page.")

# --- Index View (with team, services, and feedbacks)
def index(request):
    team_members = TeamMember.objects.all()
    services = Service.objects.all()
    feedbacks = Feedback.objects.select_related('user').order_by('-submitted_at')
    monthly_plans = PricingPlan.objects.filter(plan_type='monthly')
    yearly_plans = PricingPlan.objects.filter(plan_type='yearly')
    # pricing_plans = PricingPlan.objects.all()
    return render(request, 'index.html', {
        'team_members': team_members,
        'services': services,
        'feedbacks': feedbacks,
        'monthly_plans': monthly_plans,
        'yearly_plans': yearly_plans
        # 'pricing_plans': pricing_plans

    })
 

# from django.shortcuts import render, redirect
from django.contrib import messages
# …your other imports…

def register(request):
    if request.method == "POST":
        username  = request.POST["username"]
        email     = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("login")        

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("login")

      
        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=password1
        )
        request.session["email"] = user.email     

        messages.success(request, "Registration successful! Welcome aboard 🎉")
        return redirect("index")               

    return render(request, "login.html")

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            u = CustomUser.objects.get(email=email)
            if password == u.password:
                request.session['email'] = u.email
                return redirect('index')
            else:
                return render(request, "login.html", {'msg': 'Invalid password'})
        except CustomUser.DoesNotExist:
            return render(request, "login.html", {'msg': 'Invalid email'})

    return render(request, "login.html")

# --- Logout
def logout(request):
    request.session.flush()
    return redirect('login')

# --- Feedback Submission
def feedback_view(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        message = request.POST.get('message')
        session_email = request.session.get('email')

        if not session_email:
            messages.error(request, "Please login to submit feedback.")
            return redirect('login')

        try:
            custom_user = CustomUser.objects.get(email=session_email)
            Feedback.objects.create(
                user=custom_user,
                rating=rating,
                message=message
            )
            messages.success(request, "Thank you for your feedback!")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found. Please login again.")

        return redirect('feedback')

    return render(request, 'feedback.html')

# --- Profile Routing
def profile_router(request):
    if 'email' not in request.session:
        return redirect('login')

    return redirect('view_profile')

# --- Profile Creation (now edit only)
def create_profile(request):
    return redirect('edit_profile')

# --- Profile Viewing
def view_profile(request):
    if 'email' not in request.session:
        return redirect('login')

    current_user = CustomUser.objects.get(email=request.session['email'])
    return render(request, 'profile_view.html', {'u': current_user})

# --- Profile Editing
def edit_profile(request):
    if 'email' not in request.session:
        return redirect('login')

    current_user = CustomUser.objects.get(email=request.session['email'])

    if request.method == 'POST':
        current_user.full_name = request.POST.get('full_name')
        current_user.phone = request.POST.get('phone')
        current_user.bio = request.POST.get('bio')
        if request.FILES.get('profile_image'):
            current_user.profile_image = request.FILES['profile_image']
        current_user.save()
        return redirect('view_profile')

    return render(request, 'profile_form.html', {'u': current_user})

# --- Optional: Testimonials Page
def testimonials_view(request):
    feedbacks = Feedback.objects.select_related('user').all()
    return render(request, 'your_template.html', {'feedbacks': feedbacks})

# --- Contact Message
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, "Your message has been sent. Thank you!")
        return redirect('index')

    return render(request, 'index.html')
# views.py
# views.py


def consultation_view(request):
    if request.method == "POST":
        name    = request.POST["name"]
        email   = request.POST["email"]
        phone   = request.POST.get("phone", "")
        service = request.POST["service"]

        # save to DB
       
        ConsultationRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            service=service,
        )

        # send e‑mail to the visitor
        subject = "✅ Your free consultation is booked!"
        message = (
            f"Hi {name},\n\n"
            f"Thank you for requesting a free {service} consultation.\n"
            "Our team will contact you within 24 hours to schedule the call.\n\n"
            "Best regards,\n"
            "The Consulting Team"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # put a one‑time Django message on the session
        messages.success(
            request,
            "✅ Thank you! We’ll call you soon for your free consultation."
        )

        # redirect wherever you want to land after submit
        return redirect("index")          # or redirect(request.META["HTTP_REFERER"])

    # if someone hits /consultation/ with GET, just bounce home
    return redirect("index")
    



from django.shortcuts import render, get_object_or_404

def information_view(request, plan_id, plan_type):
    plan = get_object_or_404(PricingPlan, id=plan_id, plan_type=plan_type)
    return render(request, 'information.html', {
        'plan': plan,
        'plan_type': plan_type.capitalize()
    })
