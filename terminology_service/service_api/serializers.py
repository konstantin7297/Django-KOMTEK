from rest_framework import serializers

from .models import Directory, DirectoryElement


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
