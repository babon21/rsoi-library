from rest_framework import serializers
from .models import GenreStat, UserStat


class GenreStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreStat
        fields = ['genre', 'count']


class UserStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStat
        fields = ['user_id', 'taken_count', 'expired_count', 'in_time']
