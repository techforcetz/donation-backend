from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Charity, CharityUploads, CharityPhases, Donations

@admin.register(Charity)
class CharityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "bank_acc", "amount_needed", "deadline")
    search_fields = ("name", "user__username")
    list_filter = ("deadline",)

@admin.register(CharityUploads)
class CharityUploadsAdmin(admin.ModelAdmin):
    list_display = ("id", "charity", "document", "uploaded_date")
    search_fields = ("charity__name",)
    list_filter = ("uploaded_date",)

@admin.register(CharityPhases)
class CharityPhasesAdmin(admin.ModelAdmin):
    list_display = ("id", "charity", "description", "amount")
    search_fields = ("charity__name", "description")

@admin.register(Donations)
class DonationsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "charity", "amount","vendor","phone", "donated_at")
    search_fields = ("user__username", "charity__name")
    list_filter = ("donated_at",)
