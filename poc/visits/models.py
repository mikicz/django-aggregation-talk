from django.db import models
from django_pgviews import view as pg
# Create your models here.


class PageVisit(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    section = models.CharField(max_length=100)
    visit_time = models.DateTimeField()


class VisitsSummaryView(pg.View):
    user = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING)
    section = models.CharField(max_length=100)
    visit_date = models.DateField()
    count = models.IntegerField()

    sql = """
    SELECT 
           ROW_NUMBER() over () as id,
           "visits_pagevisit"."user_id",
           "visits_pagevisit"."section",
           ("visits_pagevisit"."visit_time" AT TIME ZONE 'UTC')::date AS "visit_date",
           COUNT("visits_pagevisit"."id") AS "count"
    FROM "visits_pagevisit"
    GROUP BY "visits_pagevisit"."user_id",
              "visits_pagevisit"."section",
              ("visits_pagevisit"."visit_time" AT TIME ZONE 'UTC')::date
    """
