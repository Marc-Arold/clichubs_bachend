from django.contrib import admin
from .models import Balance
# Register your models here.

class BalanceAdmin(admin.ModelAdmin):
    list_filter = ('balance_date',)
    list_display = ('gambler','balance_globale','balance_transfert','balance_bonus','balance_date',)

admin.site.register(Balance,BalanceAdmin)