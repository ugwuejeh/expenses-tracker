from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .models import Userprofile
import uuid
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Sum
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View, ListView
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .models import *
import uuid
from django.contrib import messages
from django.db.models import Q
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
# from django.urls import reverse_lazy
from django.db import IntegrityError
# from django.utils.text import slugify
from django.http import JsonResponse


# Create your views here.






class Dashboard(View):
    template_name = 'index.html'

    def get(self, request):
        # Calculate sum total of all category incomes
        sum_total_income = Incomecategory.objects.aggregate(
            sum_total_income=Sum('income__amount')
        )['sum_total_income'] or 0

        # Calculate sum total of all category expenses
        sum_total_expense = Expensescategory.objects.aggregate(
            sum_total_expense=Sum('expenses__amount')
        )['sum_total_expense'] or 0

        # Calculate percentage expenses in relation to total income
        total_expense_percentage = (sum_total_expense / sum_total_income) * 100 if sum_total_income != 0 else 0

        context = {
            'sum_total_income': sum_total_income,
            'sum_total_expense': sum_total_expense,
            'total_expense_percentage': total_expense_percentage,
        }
        return render(request, self.template_name, context)
    
    
    def get_json_data(self):
        # Function to return JSON data for AJAX requests
        sum_total_income = Incomecategory.objects.aggregate(
            sum_total_income=Sum('income__amount')
        )['sum_total_income'] or 0

        sum_total_expense = Expensescategory.objects.aggregate(
            sum_total_expense=Sum('expenses__amount')
        )['sum_total_expense'] or 0

        total_expense_percentage = (sum_total_expense / sum_total_income) * 100 if sum_total_income != 0 else 0

        return JsonResponse({
            'sum_total_income': sum_total_income,
            'sum_total_expense': sum_total_expense,
            'total_expense_percentage': total_expense_percentage,
        })

# class Dashboard(View):
#     template_name = 'index.html'

#     def get(self, request):
#         # Calculate sum total of all category incomes
#         sum_total_income = Incomecategory.objects.aggregate(
#             sum_total_income=Sum('income__amount')
#         )['sum_total_income'] or 0

#         context = {'sum_total_income': sum_total_income}
#         return render(request, self.template_name, context)

# views.py





class Signup(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html')
    
    def post(self, request):
        if request.method == 'POST':
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password != password2:
              return render(request, 'signup.html', {'error': 'Passwords do not match'})

            # Create a user without saving it to the database
            user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
            # Generate a link for completing the registration
            activation_key = str(uuid.uuid4())
            profile = Userprofile.objects.create(user=user, activation_key=activation_key)
            registration_link = f"http://127.0.0.1:8000/register/{profile.activation_key}/"

            # Send registration link to the user's email
            send_mail(
                'Complete Your Registration',
                f'Use this link to complete your registration: {registration_link}',
                'joshlove00001@gmail.com',
                [email],
                fail_silently=False,
            )
            return HttpResponse('Check your mail for link to complete your registration')
        
        #  return render(request, 'register.html')


class RegisterActivationView(View):
    def get(self, request, activation_key):
        try:
            # Find the user profile with the given activation key
            profile = Userprofile.objects.get(activation_key=activation_key)
            # Activate the associated user
            user = profile.user
            user.is_active = True
            user.save()
            # Render a success page or redirect to registration page
            messages.success(request, 'Activation successful. You can now continue with your registration.')
            # return redirect('register')
            return render(request, 'register.html')

        except Userprofile.DoesNotExist:
            # Render an error page or redirect to an error page
            messages.error(request, 'Invalid activation key. Please contact support.')
            return redirect('error_page')

    
class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # Retrieve data from the form
            fullname = request.POST.get('fullname')
            address = request.POST.get('address')
            dob = request.POST.get('dob')

            # Retrieve the existing user based on the provided primary key (pk)
            user_pk = kwargs.get('pk')
            user = User.objects.get(pk=user_pk)

            # Create or update the user profile
            profile, profile_created = Userprofile.objects.get_or_create(user=user)
            profile.fullname = fullname
            profile.address = address
            profile.dob = dob
            profile.save()
            return redirect('login')  # Redirect to a success page or login page
        return render(request, 'register.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html') 
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return HttpResponse('Username and password are required', status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('Username not found', status=404)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse('Incorrect password, try again', status=401)
    
         
def Logout(request):
    logout(request)
    return redirect('login')
 


# Step 1: User requests password reset
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Step 2: Token generation and email sending
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
    

            token = default_token_generator.make_token(user)
            user.reset_password_token = token
            user.reset_password_token_created_at = timezone.now()
            user.save()
                      
            # reset_link = f"http://127.0.0.1:8000/reset_password/?token={token}"  # Your reset URL
            reset_link = f"http://{request.get_host()}/reset/{uid}/{token}/"
            send_mail(
                'Password Reset',
                f'Click the link to reset your password: {reset_link}',
                'joshlove00001@gmail.com',
                [email],
                fail_silently=False,
            )
            # Show a success message or redirect to a confirmation page
            return HttpResponse('Check your mail for link to reset your password')
    # Inside your view
    return render(request, 'forgot_password.html')


# Step 3: Reset password page
def reset_password(request):
    token = request.GET.get('token')
    user = User.objects.filter(reset_password_token=token).first()
    if user and default_token_generator.check_token(user, token):
        # Token is valid, check if it's expired (e.g., expires in 1 hour)
        if timezone.now() - user.reset_password_token_created_at < timezone.timedelta(hours=1):
            # Show password reset form
            return render(request, 'reset_password.html', {'token': token})
        else:
            # Token expired, handle accordingly (e.g., show an error message)
            pass
    else:
        # Invalid token, handle accordingly (e.g., show an error message)
        pass



class ResetPasswordConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            # Allow the user to reset the password
            # Redirect to the password reset form
            return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})
        else:
            # Invalid link or token
            return render(request, 'invalid_reset_link.html')

# Step 4: Password update
def update_password(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        password = request.POST.get('password')
        user = User.objects.filter(reset_password_token=token).first()
        if user and default_token_generator.check_token(user, token):
            # Token is valid, check if it's expired (e.g., expires in 1 hour)
            if timezone.now() - user.reset_password_token_created_at < timezone.timedelta(hours=1):
                # Update user's password and invalidate token
                user.set_password(password)
                user.reset_password_token = None
                user.reset_password_token_created_at = None
                user.save()
                
                
                # Redirect to login page or show a success message
                return render(request, 'password_reset_success.html')
            else:
                # Token expired, handle accordingly (e.g., show an error message)
                pass
        else:
            # Invalid token, handle accordingly (e.g., show an error message)
            pass
    # Handle other cases (GET request, invalid form submission, etc.)
#     from django.contrib.auth.models import User
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.utils import timezone
# from django.contrib.auth.tokens import default_token_generator
# from .models import UserProfile

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_profile = Userprofile.objects.filter(user__email=email).first()
        if user_profile:
            # Step 2: Token generation and email sending
            uid = urlsafe_base64_encode(force_bytes(user_profile.user.pk))

            token = default_token_generator.make_token(user_profile.user)
            user_profile.reset_password_token = token
            user_profile.reset_password_token_created_at = timezone.now()
            user_profile.save()
            
            # Send the reset link via email and handle the rest of the logic
            # ...

# Function for creating new income
class IncomeCreateView(View):
    template_name = 'incoexp/income_create.html'

    def get(self, request):
        categories = Incomecategory.objects.all()
        return render(request, self.template_name, {'categories': categories})

    def post(self, request):
        # Extract data from the request
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        incometype_id = request.POST.get('incometype')

        # Create a new income entry
        Income.objects.create(
            description=description,
            amount=amount,
            date=date,
            incometype_id=incometype_id
        )
        return redirect('income-list')

# To view list of all income
class IncomeListView(ListView):
    model = Income
    template_name = 'incoexp/income_list.html'
    context_object_name = 'income_list'


# For income category creation
class IncomeCategoryCreateView(View):
    template_name = 'incoexp/incomecategory_create.html'
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        try:
            category = Incomecategory.objects.create(name=name)
        except IntegrityError:
            error = "Category with this name already exists."
            return render(request, self.template_name, {'error': error})
        return redirect('incomecategory-list')

# This is for viewing income categories
class IncomeCategoryListView(View):
    template_name = 'incoexp/incomecategory_list.html'
    def get(self, request):
        income_categories = Incomecategory.objects.all()
        return render(request, self.template_name, {'income_categories': income_categories})



# Function for creating new expenses
class ExpensesCreateView(View):
    template_name = 'incoexp/expenses_create.html'

    def get(self, request):
        categories = Expensescategory.objects.all()
        return render(request, self.template_name, {'categories': categories})

    def post(self, request):
        # Extract data from the request
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        expensetype_id = request.POST.get('expensetype')

        # Check if expensetype_id is provided
        if expensetype_id is not None:
            # Create a new expense entry
            Expenses.objects.create(
                description=description,
                amount=amount,
                date=date,
                expensetype_id=expensetype_id
            )
            return redirect('expenses_list')
        else:
            # Handle the case where expensetype_id is not provided
            messages.error(request, 'Expenses Type is required.')
            return redirect('expenses-create')  # Redirect back to the create form with an error message




# To view list of all expenses
class ExpensesListView(ListView):
    model = Expenses
    template_name = 'incoexp/expenses_list.html'
    context_object_name = 'expenses_list'

# For expenses category creation
class ExpensesCategoryCreateView(View):
    template_name = 'incoexp/expensescategory_create.html'
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        try:
            category = Expensescategory.objects.create(name=name)
        except IntegrityError:
            error = "Category with this name already exists."
            return render(request, self.template_name, {'error': error})
        return redirect('expensescategory-list')

# This is for viewing expenses categories
class ExpensesCategoryListView(View):
    template_name = 'incoexp/expensescategory_list.html'
    def get(self, request):
        expense_categories = Expensescategory.objects.all()
        return render(request, self.template_name, {'expenses_categories': expense_categories})


class TotalIncomeByCategoryView(View):
    template_name = 'incoexp/total_income.html'

    def get(self, request):
        # Calculate total income for each category
        total_income_by_category = Incomecategory.objects.annotate(
            total_income=Sum('income__amount')
        ).values('name', 'total_income')

        # Calculate sum total of all category incomes
        sum_total_income = Incomecategory.objects.aggregate(
            sum_total_income=Sum('income__amount')
        )['sum_total_income'] or 0

        context = {
            'total_income_by_category': total_income_by_category,
            'sum_total_income': sum_total_income,
        }

        return render(request, self.template_name, context)

class TotalExpenseByCategoryView(View):
    template_name = 'incoexp/total_expense.html'

    def get(self, request):
        # Calculate total expenses for each category
        total_expense_by_category = Expensescategory.objects.annotate(
            total_expense=Sum('expenses__amount')
        ).values('name', 'total_expense')

        # Calculate sum total of all category expenses
        sum_total_expense = Expensescategory.objects.aggregate(
            sum_total_expense=Sum('expenses__amount')
        )['sum_total_expense'] or 0

        # Calculate total income for each income category
        total_income_by_category = Incomecategory.objects.annotate(
            total_income=Sum('income__amount')
        ).values('name', 'total_income')

        # Calculate sum total of all category incomes
        sum_total_income = Incomecategory.objects.aggregate(
            sum_total_income=Sum('income__amount')
        )['sum_total_income'] or 0

        # Calculate total expenses as a percentage of total income
        total_expense_percentage = (sum_total_expense / sum_total_income) * 100 if sum_total_income != 0 else 0

        context = {
            'total_expense_by_category': total_expense_by_category,
            'sum_total_expense': sum_total_expense,
            'total_income_by_category': total_income_by_category,
            'sum_total_income': sum_total_income,
            'total_expense_percentage': total_expense_percentage,
        }

        return render(request, self.template_name, context)