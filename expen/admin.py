from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Userprofile)

admin.site.register(Expensescategory)

admin.site.register(Incomecategory)

admin.site.register(Income)

admin.site.register(Expenses)

admin.site.register(IncomeReset)

admin.site.register(ExpenseReset)






# from django.contrib import admin
# from .models import Profile,IncomeCategory,ExpenseCategory,Income,Expense,IncomeReset,ExpenseReset


# # Register your models here.
# admin.site.register(Profile)
# admin.site.register(ExpenseCategory)
# admin.site.register(IncomeCategory)
# admin.site.register(Income)
# admin.site.register(Expense)
# admin.site.register(IncomeReset)
# admin.site.register(ExpenseReset)