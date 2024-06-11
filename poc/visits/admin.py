from django.contrib import admin

from visits.models import PageVisit


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ("user", "section", "visit_time")
    list_filter = ("section", "visit_time")
    list_select_related = ("user",)
