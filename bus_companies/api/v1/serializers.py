from rest_framework import serializers
from bus_companies.models import BusCompany

class BusCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusCompany
        fields = ['id', 'name', 'email', 'phone', 'address', 'active_buses_count']
        read_only_fields = ['active_buses_count']
