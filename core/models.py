from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Payment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"

class RepairCompany(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CompanyService(models.Model):
    company = models.ForeignKey(RepairCompany, on_delete=models.CASCADE, related_name="services")
    service_name = models.CharField(max_length=100)
    service_description = models.TextField()

    def __str__(self):
        return f"{self.service_name} ({self.company.name})"

class PageVisit(models.Model):
    page_name = models.CharField(max_length=200)
    visit_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.page_name} - {self.visit_count} visits"


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name} - {self.event_count} occurrences"

class Prediction(models.Model):
    service_name = models.CharField(max_length=100)
    estimated_time = models.DecimalField(max_digits=5, decimal_places=2)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_name}: {self.estimated_time} hours, {self.estimated_cost} cost"
