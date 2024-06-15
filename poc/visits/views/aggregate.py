from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions.datetime import TruncDate
from rest_framework.generics import ListAPIView
from rest_framework import serializers

from visits.models import PageVisit


class AggregateSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    section = serializers.CharField()
    visit_date = serializers.DateField()
    count = serializers.IntegerField()


class AggregateView(ListAPIView):
    serializer_class = AggregateSerializer

    def get_queryset(self):
        return (
            PageVisit.objects.annotate(visit_date=TruncDate("visit_time"))
            .values("user", "section", "visit_date")
            .annotate(count=Count("id"))
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class AggregateSerializerWithUser(serializers.Serializer):
    user_id = serializers.IntegerField(source="user__id")
    user_username = serializers.CharField(source="user__username")
    user_email = serializers.EmailField(source="user__email")
    user_first_name = serializers.CharField(source="user__first_name")
    user_last_name = serializers.CharField(source="user__last_name")

    section = serializers.CharField()
    visit_date = serializers.DateField()
    count = serializers.IntegerField()


class AggregateViewWithUser(ListAPIView):
    serializer_class = AggregateSerializerWithUser

    def get_queryset(self):
        return (
            PageVisit.objects.annotate(visit_date=TruncDate("visit_time"))
            .values(
                "user__id",
                "user__username",
                "user__email",
                "user__first_name",
                "user__last_name",
                "section",
                "visit_date",
            )
            .annotate(count=Count("id"))
        )
