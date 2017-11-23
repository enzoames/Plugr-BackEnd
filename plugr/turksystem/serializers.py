from rest_framework import serializers
from .models import *


class TurkUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurkUser
        fields = '__all__'


# ========================================================================================================================
# ========================================================================================================================
# ================================================ ROHAN ==================================================================
# ========================================================================================================================
# ========================================================================================================================
class SysDemandSerializer(serializers.ModelSerializer):
    client = TurkUserSerializer()
    class Meta:
        model = SystemDemand
        fields = '__all__'

    def create(self, validated_data):
        sysDemand = SystemDemand.objects.create(**validated_data)
        return sysDemand


class BidSerializer(serializers.ModelSerializer):
    developer = TurkUserSerializer()
    systemdemand = SysDemandSerializer()
    class Meta:
        model = Bid
        fields = '__all__'

# ========================================================================================================================
# ========================================================================================================================
# ================================================ ENZO ==================================================================
# ========================================================================================================================
# ========================================================================================================================

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurkUser
        fields = '__all__'

        def create(self, validated_data):
            data = validated_data
            print("\n\n====DATA CREATED IN SERIALIZER REGISTER:", data)
            # print(json.dumps(data, indent=4))
            register = TurkUser.objects.create(**data)
            return register
