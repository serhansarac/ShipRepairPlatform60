from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import PageVisit, Event
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Service, Payment
from .models import Payment
from .models import RepairCompany
from .models import RepairCompany
from .models import CompanyService
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Prediction
import random  # Mock data for demonstration
import datetime
import re
import joblib
import numpy as np

def home(request):
    return render(request, 'core/home.html')

def services(request):
    services = Service.objects.all()
    return render(request, 'core/services.html', {'services': services})

def payment_page(request):
    return render(request, 'core/payment.html')

@csrf_exempt
def charge(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not name or not email or not re.match(email_regex, email):
            return JsonResponse({"status": "error", "message": "Invalid name or email"})

        request.session['name'] = name
        request.session['email'] = email
        # �deme kayd�n� ekleyin
        Payment.objects.create(name=name, email=email, amount=10.00)
        return JsonResponse({"status": "success", "message": f"Payment processed for {name} ({email})"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

def generate_invoice(request):
    name = request.session.get("name", "Default Name")
    email = request.session.get("email", "default@example.com")
    context = {
        "name": name,
        "email": email,
        "amount": "$10.00",
        "date": datetime.date.today(),
    }
    html = render_to_string("core/invoice.html", context)
    pdf = HTML(string=html).write_pdf()
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
    return response

def payment_history(request):
    payments = Payment.objects.all().order_by('-date')  # �demeleri tarihe g�re s�rala
    return render(request, 'core/payment_history.html', {'payments': payments})

def repair_companies(request):
    companies = RepairCompany.objects.all()
    return render(request, 'core/repair_companies.html', {'companies': companies})

def company_services(request, company_id):
    # �irketi al�n
    company = get_object_or_404(RepairCompany, id=company_id)
    # �irketin t�m hizmetlerini al�n
    services = company.services.all()
    # �ablonu render edin
    return render(request, 'core/company_services.html', {'company': company, 'services': services})

def compare_services(request):
    # T�m hizmetleri veritaban�ndan al�n
    all_services = CompanyService.objects.select_related('company').all()
    return render(request, 'core/compare_services.html', {'services': all_services})

def analytics(request):
    # Payment volume data
    current_year = datetime.datetime.now().year
    months = [
        "January", "February", "March", "April", "May", 
        "June", "July", "August", "September", 
        "October", "November", "December"
    ]
    payment_data = [
        float(Payment.objects.filter(date__year=current_year, date__month=i).aggregate(Sum('amount'))['amount__sum'] or 0)
        for i in range(1, 13)
    ]
    # Customer satisfaction data (mock data for now)
    satisfaction_data = [60, 30, 10]  # Example: 60% Satisfied, 30% Neutral, 10% Unsatisfied

    context = {
        'months': months,
        'payment_data': payment_data,
        'satisfaction_data': satisfaction_data,
    }
    return render(request, 'core/analytics.html', context)
@staff_member_required
def admin_dashboard(request):
    payments = Payment.objects.order_by('-date')[:10]  # Son 10 �deme
    total_payment = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'payments': payments,
        'total_payment': total_payment,
    }
    return render(request, 'core/admin_dashboard.html', context)
def record_visit(page_name):
    visit, created = PageVisit.objects.get_or_create(page_name=page_name)
    visit.visit_count += 1
    visit.save()

def record_event(event_name):
    event, created = Event.objects.get_or_create(event_name=event_name)
    event.event_count += 1
    event.save()

def mock_analytics(request):
    # Simulate some page visits
    record_visit("Home")
    record_visit("Services")
    record_visit("Analytics")

    # Simulate some events
    record_event("Button Click")
    record_event("Form Submit")

    # Aggregate data
    page_visits = PageVisit.objects.all()
    events = Event.objects.all()

    total_visits = page_visits.aggregate(Sum('visit_count'))['visit_count__sum'] or 0
    total_events = events.aggregate(Sum('event_count'))['event_count__sum'] or 0

    context = {
        'page_visits': page_visits,
        'events': events,
        'total_visits': total_visits,
        'total_events': total_events,
    }
    return render(request, 'core/mock_analytics.html', context)

def predict_service(request):
    if request.method == "POST":
        service_name = request.POST.get("service_name")
        
        # Simulate predictions
        estimated_time = round(random.uniform(2, 48), 2)  # Random hours between 2 and 48
        estimated_cost = round(random.uniform(100, 5000), 2)  # Random cost
        
        prediction = Prediction.objects.create(
            service_name=service_name,
            estimated_time=estimated_time,
            estimated_cost=estimated_cost,
        )
        
        return JsonResponse({
            "service_name": service_name,
            "estimated_time": estimated_time,
            "estimated_cost": estimated_cost,
        })
    
    return render(request, "core/predict_service.html")

# Load trained models
time_model = joblib.load('ml_models/time_model.pkl')
cost_model = joblib.load('ml_models/cost_model.pkl')

def predict_service(request):
    if request.method == "POST":
        service_name = request.POST.get("service_name")
        complexity = float(request.POST.get("complexity"))

        # Make predictions
        features = np.array([[complexity]])
        estimated_time = round(time_model.predict(features)[0], 2)
        estimated_cost = round(cost_model.predict(features)[0], 2)

        prediction = Prediction.objects.create(
            service_name=service_name,
            estimated_time=estimated_time,
            estimated_cost=estimated_cost,
        )
        
        return JsonResponse({
            "service_name": service_name,
            "estimated_time": estimated_time,
            "estimated_cost": estimated_cost,
        })
    
    return render(request, "core/predict_service.html")