from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from django_filters import rest_framework as filters

from visits.models import VisitsSummaryView


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class ViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = VisitsSummaryView
        fields = ["user", "section", "visit_date", "count"]


from django_filters import rest_framework as filters


class VisitsSummaryViewFilter(filters.FilterSet):
    class Meta:
        model = VisitsSummaryView
        fields = ["section", "visit_date"]


class ViewView(ListAPIView):
    serializer_class = ViewSerializer
    queryset = VisitsSummaryView.objects.select_related("user").order_by("-count")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VisitsSummaryViewFilter
