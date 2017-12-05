from rest_framework import serializers
from .models import *


class TurkUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurkUser
        fields = '__all__'

    def update(self, validated_data, instance):
        instance.resume = validated_data.get('resume', instance.resume)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.technical_skills = validated_data.get('technical_skills', instance.technical_skills)
        instance.project_experience = validated_data.get('project_experience', instance.project_experience)
        instance.interests = validated_data.get('interests', instance.interests)
        instance.recent_work = validated_data.get('recent_work', instance.recent_work)
        instance.business_credential = validated_data.get('business_credential', instance.business_credential)
        instance.save()
        return instance


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

    def create(self, validated_data):
        # print(json.dumps(data, indent=4))
        print(" ===> BidSerializer Create ")
        register = Bid.objects.create(**validated_data)
        return register


class ChosenDeveloperSerializer(serializers.ModelSerializer):
    sysdemand = SysDemandSerializer()
    developer = TurkUserSerializer()  # for dev and client

    class Meta:
        model = ChosenDeveloper
        fields = '__all__'

    def create(self, validated_data):
        print("Choosen Dev serializer")
        register = ChosenDeveloper.objects.create(**validated_data)
        return register


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
        # print(json.dumps(data, indent=4))
        register = TurkUser.objects.create(**validated_data)
        return register
