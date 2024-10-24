from django.shortcuts import render, redirect, get_object_or_404
from .forms import AppointmentForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Appointment, Payment, Test
from django.db import transaction


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')


# Register and login
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')  # Redirect to profile after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # Redirect to profile page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Diagnosis and payment integration
@login_required
def diagnosis(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                appointment = form.save()
                test = appointment.test
                Payment.objects.create(
                    user=request.user,
                    appointment=appointment,
                    test=test,
                    amount=test.amount,
                    status='Pending'
                )
            return redirect('initiate_payment', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    
    return render(request, 'add_book.html', {'form': form})


def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'dummy_payment.html', {'appointments': appointments})

@login_required
def initiate_payment(request, appointment_id):
    # Retrieve the appointment using a unique identifier
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Retrieve the test associated with the appointment
    test = appointment.test

    # Create a payment record
    payment = Payment.objects.create(
        user=request.user,
        appointment=appointment,
        test=test,
        amount=test.amount,
        status='Pending'
    )

    # Redirect to a payment success page or handle payment processing
    return render(request, 'dummy_payment.html', {'payment': payment})

# Function to fetch the amount for the selected test type
def get_test_amount(test_type):
    test_amounts = {
        'test1': 100.00,  # Example amount for Test 1
        'test2': 200.00,  # Example amount for Test 2
    }
    return test_amounts.get(test_type, 0.00)


# Dummy payment processing
@login_required
def dummy_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if request.method == 'POST':
        # Simulate payment completion
        payment.status = 'Completed'
        payment.save()
        return redirect('payment_success')  # Redirect to success page

    return render(request, 'dummy_payment.html', {'payment': payment})


@login_required
def payment_success(request):
    return render(request, 'payment_success.html')


# Profile view
@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'user_profile': user_profile})
