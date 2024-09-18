from datetime import datetime
from sqlite3 import Date

from rest_framework import serializers

from .models import Directory, DirectoryElement


class DateSerializer(serializers.Serializer):
    """ Схема для валидации даты в строковом виде """
    date = serializers.SerializerMethodField('get_date')

    @staticmethod
    def get_date(obj: str):
        year, month, day = obj.split("-")
        if datetime(int(year), int(month), int(day)):
            return Date(year=year, month=month, day=day)


class DirectorySerializer(serializers.ModelSerializer):
    """ Схема для валидации модели таблицы справочника """
    class Meta:
        model = Directory
        fields = "id", "code", "name"


class DirectoryElementSerializer(serializers.ModelSerializer):
    """ Схема для валидации модели таблицы элемента справочника """
    class Meta:
        model = DirectoryElement
        fields = "code", "value"


class CheckSerializer(serializers.Serializer):
    """ Схема для валидации входных данных при проверке существования версии """
    code = serializers.CharField()
    value = serializers.CharField()
    version = serializers.CharField()
