from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework import serializers

from visits.models import VisitsSummaryMaterializedView


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class MaterializedViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = VisitsSummaryMaterializedView
        fields = ["user", "section", "visit_date", "count"]


class MaterializedViewView(ListAPIView):
    serializer_class = MaterializedViewSerializer
    queryset = VisitsSummaryMaterializedView.objects.select_related("user").order_by(
        "-count"
    )
