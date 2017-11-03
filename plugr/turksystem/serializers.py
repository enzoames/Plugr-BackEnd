from rest_framework import serializers
from .models import *


class TurkUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurkUser
        fields = '__all__'
