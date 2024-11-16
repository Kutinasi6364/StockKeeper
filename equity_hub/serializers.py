from rest_framework import serializers
from .models import EquityHub


class EquityHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquityHub
        fields = '__all__'