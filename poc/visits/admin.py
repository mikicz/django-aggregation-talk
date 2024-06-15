from django.contrib import admin

from visits.models import PageVisit, VisitsSummaryView, VisitsSummaryMaterializedView


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ("user", "section", "visit_time")
    list_filter = ("section", "visit_time")
    list_select_related = ("user",)


@admin.register(VisitsSummaryView)
class VisitsSummaryViewAdmin(admin.ModelAdmin):
    list_display = ("user", "section", "visit_date", "count")
    list_filter = ("section", "visit_date")
    list_select_related = ("user",)


@admin.register(VisitsSummaryMaterializedView)
class VisitsSummaryMaterializedViewAdmin(admin.ModelAdmin):
    list_display = ("user", "section", "visit_date", "count")
    list_filter = ("section", "visit_date")
    list_select_related = ("user",)
