from rest_framework import serializers
from city.models import City, Province, Terminal

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'province', 'is_active', 'created_at']


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name']


class TerminalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Terminal
        fields = ['id', 'name', 'address', 'phone', 'is_active', 'created_at']
        