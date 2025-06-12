from rest_framework import serializers
from city.models import City, Province, Terminal

class CitySerializer(serializers.ModelSerializer):
    province = serializers.CharField(source='province.name', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = City
        fields = ['id', 'name', 'province', 'is_active', 'created_at']


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name']


class TerminalSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Terminal
        fields = ['id', 'city', 'name', 'address', 'phone', 'is_active', 'created_at']
        