from rest_framework import serializers
from .models import UserMonitoring


class MonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMonitoring
        fields = ['current_count', 'max_count']
