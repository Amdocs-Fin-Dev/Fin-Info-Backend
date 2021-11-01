from django.contrib import admin
from .models import Account, Invest, Portfolio
# Register your models here.

admin.site.register(Account)
admin.site.register(Portfolio)
admin.site.register(Invest)