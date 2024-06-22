---
lineNumbers: true
download: true
theme: dracula
highlighter: shiki
favicon: '/favicon.png'
fonts:
  sans: "Barlow"
---

# **Aggregating data in Django** 
# **using database views**

### a talk by Mikuláš Poul
### July 10th, 2024 - Europython

---

# About me

- he/him, go by Miki
- Born in the Czech Republic
- Live in London, UK

<v-clicks>

- Coding in Python for more years than not
- Have been using Django for 10 years
- Staff Engineer at [<img src="/xelix.svg" style="display: inline; height: 25px; margin-top: -10px" />](https://xelix.com/)
- [www.mikulaspoul.cz](https://www.mikulaspoul.cz/)

</v-clicks>

<!--
Mention all links & relevant details are on mikulaspoul, plus a blog and link to this talk
-->

--- 

# Contents

- A brief overview of aggregation using native Django
- Introduction to database views
- Introduction to the package `django-pgviews-redux`
- Introduction to materialized views

<v-click>

- Soft pre-requisites: Django & SQL

</v-click>

---

# Data Aggregation In Django

- Aggregation - combining multiple pices of information in a single result

<v-clicks>

- Any sort of statistics and reporting usually involve aggregation
- An aggregation method everyone has used is queryset's `.count()`

</v-clicks>


---

# Let's define a model

```python
class PageVisit(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    section = models.CharField(max_length=100)
    visit_time = models.DateTimeField()

```

---

# Data Aggregation In Django

- An aggregation method everyone has used is queryset's `.count()`

<v-click>

```python
>> PageVisit.objects.count()
50741

```
</v-click>

<v-click>

- This is syntactic sugar around `.aggregate()`
- That method runs aggregation on the entire queryset

```python
>> PageVisit.objects.aggregate(count=Count("*"))["count"] or 0
0
```

</v-click>

---

# Data Aggregation In Django

- There's many different aggregation functions 

```python
>> from django.db.models import Max
>> PageVisit.objects.filter(section="index").aggregate(Max("visit_time"))
{'visit_time__max': datetime(2024, 6, 15, 12, 15, 28, 138712, tzinfo=datetime.timezone.utc)}
```

<v-click>

```python
>> from django.db.models import Min
>> PageVisit.objects.filter(section="index").aggregate(Min("visit_time"))
{'visit_time__min': datetime.datetime(2024, 6, 1, 0, 2, 22, 37100, tzinfo=datetime.timezone.utc)}
```

</v-click>

<v-clicks>

- Other methods include `Sum`, `Avg`, `StdDev`
- You can define your own

</v-clicks>

<!--
Aggregate returns a dictionary
-->

---

# Data Aggregation In Django

- `.annotate()` aggregates per item in the queryset

```python
>> qs = User.objects.filter(is_staff=False).annotate(Count("pagevisit"))
>> qs[0].pagevisit__count
93
```

<v-click>

- `.annotate()` in combination with `.values()` aggregates per unique value

```python
>> PageVisit.objects.values("section").annotate(Max("visit_time"))
<QuerySet [
    {'section': 'dashboard', 'visit_time__max': datetime(2024, 6, 15, 12, 15, 29, 612511, tzinfo=timezone.utc)}, 
    {'section': 'settings', 'visit_time__max': datetime(2024, 6, 15, 12, 16, 56, 344716, tzinfo=timezone.utc)},
    {'section': 'index', 'visit_time__max': datetime(2024, 6, 15, 12, 15, 28, 138712, tzinfo=timezone.utc)}]
>
 
```

</v-click>
---

# Let's build something!

<!-- TODO make central -->

--- 

# Let's build something!

Let's build an API which shows section visits per user pay day.

<v-click>

```python
class AggregateView(ListAPIView):
    serializer_class = AggregateSerializer

    def get_queryset(self):
        return (
            PageVisit.objects.annotate(visit_date=TruncDate("visit_time"))
            .values("user", "section", "visit_date")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

```
</v-click>

---

# Let's build something!

Let's build an API which shows section visits per user pay day.

```python
class AggregateSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    section = serializers.CharField()
    visit_date = serializers.DateField()
    count = serializers.IntegerField()
```

<v-click>

```json
[
    {
      "user": 688,
      "section": "index",
      "visit_date": "2024-06-12",
      "count": 38
    },
    ...
]
```

</v-click>

---

# Under the hood

```sql
SELECT "visits_pagevisit"."user_id",
       "visits_pagevisit"."section",
       ("visits_pagevisit"."visit_time" AT TIME ZONE 'UTC')::date AS "visit_date",
       COUNT("visits_pagevisit"."id")                             AS "count"
FROM "visits_pagevisit"
GROUP BY "visits_pagevisit"."user_id",
         "visits_pagevisit"."section",
         3       --- refers to visit date
ORDER BY 4 DESC  --- refers to count
```

---

# Downsides of the django aggregation

Despite being powerful, there are downsides

<v-clicks>

- The values returned are dictionaries, not objects
- Foreign keys are primary-keys only
</v-clicks>

<v-click>

```python
PageVisit.objects.annotate(visit_date=TruncDate("visit_time")).values(
    "user_id", 
    "user__email",
    "user__first_name",
    "user__last_name",
    "section", 
    "visit_date",
)
```

</v-click>

---

# Downsides of the django aggregation

Despite being powerful, there are downsides

- The values returned are dictionaries, not objects
- Foreign keys are primary-keys only
-  Displaying needs to be fairly manual

<v-clicks>

- Reusing the aggregation is tricky 

</v-clicks>

---

# Database Views

<!--- TODO make central --->

---

# Database Views

- A virtual table in database defined by a query

<v-clicks>

- Behaves like a normal table for SELECT
- Evaluates every single time
- Just syntactic sugar
- Supported by most common relational databases
- Does not use any extra disk space

</v-clicks>

---

# Database Views

```sql {all|1|2-4,7-9|5|6|all}
CREATE VIEW visits_visitssummary AS
SELECT "visits_pagevisit"."user_id",
       "visits_pagevisit"."section",
       ("visits_pagevisit"."visit_time" AT TIME ZONE 'UTC')::date AS "visit_date",
       COUNT("visits_pagevisit"."id") AS "count"
FROM "visits_pagevisit"
GROUP BY "visits_pagevisit"."user_id",
          "visits_pagevisit"."section",
          ("visits_pagevisit"."visit_time" AT TIME ZONE 'UTC')::date
```

<v-click>
But OK, how do I use this in Django?
</v-click>

<!--
TODO: make it central and bigger
--> 

---

# Enter django-pgviews-redux

<!--
TODO: Make this section header
-->

---

# Enter django-pgviews-redux

- Library to add good support for database views to Django

<v-clicks>

- Maintaned primarily by me at Xelix
- Fork of an earlier library called django-pgviews by Pebble 
- Support for modern Python and Django, with extra features
- Postgres specific

</v-clicks>

---

# Using django-pgviews-redux

<v-click>

```bash
$ poetry add django-pgviews-redux
```

</v-click>

<v-click>

```python
INSTALLED_APPS = [
    ...
    "django_pgviews",
]
```
</v-click>

<v-click>

```bash
$ python manage.py sync_pgviews
```

</v-click>

---

# Defining a view

```python {all|1,3|9-19|10|4-8|all}
from django_pgviews.view import View

class VisitsSummaryView(View):
    user = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING)
    section = models.CharField(max_length=100)
    visit_date = models.DateField()
    count = models.IntegerField()

    sql = """
    SELECT ROW_NUMBER() over () as id,  --- Django requires a primary key, id by default
           "visits_pagevisit"."user_id",
           "visits_pagevisit"."section",
           ("visits_pagevisit"."visit_time" AT TIME ZONE 'UTC')::date AS "visit_date",
           COUNT("visits_pagevisit"."id") AS "count"
    FROM "visits_pagevisit"
    GROUP BY "visits_pagevisit"."user_id",
              "visits_pagevisit"."section",
              ("visits_pagevisit"."visit_time" AT TIME ZONE 'UTC')::date
    """
```

--- 

# Use the view

```python {all|3|all}
class ViewView(ListAPIView):
    serializer_class = ViewSerializer
    queryset = VisitsSummaryView.objects.select_related("user").order_by("-count")
```

<v-click>

```python {all|11,12|8,1-4|all}
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class ViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = VisitsSummaryView
        fields = ["user", "section", "visit_date", "count"]
```

</v-click>

---

# Use the view

```json

[
    {
        "user": {
            "id": 688,
            "username": "paul29",
            "email": "bonniechase@yahoo.com",
            "first_name": "Jennifer",
            "last_name": "Coleman"
        },
        "section": "index",
        "visit_date": "2024-06-12",
        "count": 38
    },
    ...
]
```

---

# Under the hood

```sql {all|12|1-5|6-11,13|14|all}
SELECT "visits_visitssummaryview"."id",
       "visits_visitssummaryview"."user_id",
       "visits_visitssummaryview"."section",
       "visits_visitssummaryview"."visit_date",
       "visits_visitssummaryview"."count",
       "auth_user"."id",
       "auth_user"."first_name",
       "auth_user"."last_name",
       "auth_user"."email",
       "auth_user"."username"
       --- more of the user fields ---
FROM "visits_visitssummaryview"
INNER JOIN "auth_user" ON ("visits_visitssummaryview"."user_id" = "auth_user"."id")
ORDER BY "visits_visitssummaryview"."count" DESC
```

---

# Issues

<v-clicks>

- The values returned are dictionaries, not objects
  - Returns instances of the view model 
- Foreign keys are primary-keys only
  - Can lazy load related objects, select related / prefetch related 
- Displaying needs to be fairly manual
  - Django & library can use the defined fields to auto-discover 
- Reusing the aggregation is tricky
  - Aggregation is defined just once in model

</v-clicks>

<!-- TODO: investigate different point icon -->

---

# Other features

<v-click>

- Admin? Sure!
```python
@admin.register(VisitsSummaryView)
class VisitsSummaryViewAdmin(admin.ModelAdmin):
    list_display = ("user", "section", "visit_date", "count")
    list_filter = ("section", "visit_date")
    list_select_related = ("user",)
```

</v-click>

<v-click>

- Django Filters? Sure!
```python
from django_filters import rest_framework as filters

class VisitsSummaryViewFilter(filters.FilterSet):
    class Meta:
        model = VisitsSummaryView
        fields = ["section", "visit_date"]
```

</v-click>


---

# Inside the engine under the hood

```sql {all|8-18}
SELECT summary."id",
       summary."user_id",
       summary."section",
       summary."visit_date",
       summary."count",
       "auth_user"."id"
       --- more of the user fields ---
FROM (
    SELECT ROW_NUMBER() over () as id,
           "visits_pagevisit"."user_id",
           "visits_pagevisit"."section",
           ("visits_pagevisit"."visit_time" AT TIME ZONE 'UTC')::date AS "visit_date",
           COUNT("visits_pagevisit"."id") AS "count"
    FROM "visits_pagevisit"
    GROUP BY "visits_pagevisit"."user_id",
              "visits_pagevisit"."section",
              ("visits_pagevisit"."visit_time" AT TIME ZONE 'UTC')::date
) as summary
INNER JOIN "auth_user" ON (summary."user_id" = "auth_user"."id")
ORDER BY summary."count" DESC
```

---

# Inside the engine under the hood

Ultimately, it can be quite slow if the underlying query is slow.

<!--
TODO: make central
-->

---

# Materialized View

<!-- TODO: make central -->

---

# Materialized View

- Stores the query result in a temporary table
- On update of underlying data it becomes stale
- The view needs to be explicitly refreshed
- Good when you don't care data is out of date
- Good when you have batch processes updating data
- Bad when need to refresh often and data is big
- Does use extra storage space
- Can add indexes

---

# Defining a materialized view

```sql
CREATE MATERIALIZED VIEW materialized_summary AS
SELECT ...
```

---

# Defining a materialized view

```python {all|1,3}
from django_pgviews.view import MaterializedView

class VisitsSummaryMaterializedView(MaterializedView):
    user = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING)
    section = models.CharField(max_length=100)
    visit_date = models.DateField()
    count = models.IntegerField()

    sql = """
    SELECT ROW_NUMBER() over () as id,  --- Django requires a primary key, id by default
           "visits_pagevisit"."user_id",
           "visits_pagevisit"."section",
           ("visits_pagevisit"."visit_time" AT TIME ZONE 'UTC')::date AS "visit_date",
           COUNT("visits_pagevisit"."id") AS "count"
    FROM "visits_pagevisit"
    GROUP BY "visits_pagevisit"."user_id",
              "visits_pagevisit"."section",
              ("visits_pagevisit"."visit_time" AT TIME ZONE 'UTC')::date
    """
```

---

# Syncing & refreshing the view

<v-click>
```bash
$ python manage.py sync_pgviews
INFO [django_pgviews.view:254] pgview created materialized view visits_visitssummarymaterializedview (default schema)
INFO [django_pgviews.sync_pgviews:119] pgview visits.VisitsSummaryMaterializedView created
```
</v-click>

<v-click>

```bash
$ python manage.py refresh_pgviews
INFO [django_pgviews.sync_pgviews:149] pgview visits.VisitsSummaryMaterializedView refreshed
```

</v-click>

<v-click>

```python
VisitsSummaryMaterializedView.refresh()
```

</v-click>

---

# Using materialized views

Exactly the same as normal view!

<!-- todo make central -->

---

# Other view usages

- Views do not need to aggregate data
  - This talk used aggregated examples
  - A view can be 1-1 with extra calculated fields or de-normalised fields
  - It could be expansive rather than reductive
- Backwards compatability
- Stored expensive calculated fields

<!--

-->

---

# Conclusion

- Database views can make it easier to develop your apps
- They have pros and cons
- You can use `django-pgviews-redux` to integrate views in your app

---
layout: statement
---

# Questions?

---
layout: center
class: "text-center"
---

# Slides

TODO!

<img src="/qr_link.png" style="height: 300px" />

[Web](https://www.mikulaspoul.cz/talks/django-aggregation-talk/) / [Source](https://github.com/mikicz/django-aggregation-talk/)
