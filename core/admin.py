from django.contrib import admin
from .models import Service, Payment, RepairCompany, CompanyService,Prediction

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('name', 'email')
    date_hierarchy = 'date'

    def total_payment_amount(self, request):
        from django.db.models import Sum
        total = Payment.objects.aggregate(Sum('amount'))['amount__sum']
        return total or 0

    total_payment_amount.short_description = "Total Payment Amount"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_payment'] = self.total_payment_amount(request)
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(RepairCompany)
class RepairCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'phone_number', 'created_at')
    search_fields = ('name', 'contact_email')
    list_filter = ('created_at',)


@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'company', 'service_description')
    search_fields = ('service_name', 'company__name')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("service_name", "estimated_time", "estimated_cost", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("service_name",)