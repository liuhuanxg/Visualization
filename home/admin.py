from django.contrib import admin
from  .models import LongitudeLatitude


@admin.register(LongitudeLatitude)
class LongitudeLatitudeAdmin(admin.ModelAdmin):
    list_display = ["longitude", "latitude"]
    search_fields = ["longitude", "latitude"]

    def save_model(self, request, obj, form, change):
        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")
        l = LongitudeLatitude.objects.filter(longitude=longitude,latitude=latitude)
        if l.exists():
            pass
        else:
            super(LongitudeLatitudeAdmin, self).save_model(request, obj, form, change)