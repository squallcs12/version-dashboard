from rest_framework import serializers

from dashboard.models import ServiceDeploy


class ServiceDeploySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDeploy
        fields = '__all__'
