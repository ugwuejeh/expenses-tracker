from django.urls import path
from .views import *


urlpatterns = [
    # path('', Dashboard.as_view(), name='dashboard'),
    # path('signup/', Signup.as_view(), name='signup'),
    # path('register/<int:pk>', Register.as_view(), name='register'),
    # # path('register', Register.as_view(), name='register'),
    # path('login', Login.as_view(), name='login'),
    # path('logout/', Logout, name='logout'),
    # # path('passwordreset', ForgotPassword.as_view(), name='resetpassword'),
    # path('register/<str:activation_key>/', RegisterActivationView.as_view(), name='register_activation'),
    # # path('logout', Logout, name='logout'),


    # path('details_blog/<int:pk>', Blog_details.as_view(), name='details'),
    # path('categories/<slug:category_slug>', Categories.as_view(), name='category'),

    # URL for requesting password reset
    path('forgot_password/', forgot_password, name='forgot_password'),

    # URL for resetting password (with token)
    path('reset_password/', reset_password, name='reset_password'),

    # URL for updating password after reset
    path('update_password/', update_password, name='update_password'),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),


    path('', Login.as_view(), name='login'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('signup/', Signup.as_view(), name='signup'),
    path('register/<int:pk>/', Register.as_view(), name='register'),
    # path('register', Register.as_view(), name='register'),
    path('logout/', Logout, name='logout'),
    path('register/<str:activation_key>/', RegisterActivationView.as_view(), name='register_activation'),
    path('incomecreate/', IncomeCreateView.as_view(), name='incomecreate'),
    path('income/', IncomeListView.as_view(), name='income-list'),
    path('incomecategorycreate/', IncomeCategoryCreateView.as_view(), name='incomecategory-create'),
    path('incomecategorylist/', IncomeCategoryListView.as_view(), name='incomecategory-list'),
    path('expensescreate/', ExpensesCreateView.as_view(), name='expensescreate'),
    path('expenses/', ExpensesListView.as_view(), name='expenses_list'),
    path('expensecategorycreate/', ExpensesCategoryCreateView.as_view(), name='expensecategory-create'),
    path('expensecategorylist/', ExpensesCategoryListView.as_view(), name='expensescategory-list'),
    path('total-income-by-category/', TotalIncomeByCategoryView.as_view(), name='total-income-by-category'),
    path('total_expense_by_category/', TotalExpenseByCategoryView.as_view(), name='total_expense_by_category'),
    # path('logout', Logout, name='logout'),


    # path('details_blog/<int:pk>', Blog_details.as_view(), name='details'),
    # path('categories/<slug:category_slug>', Categories.as_view(), name='category'),
]


