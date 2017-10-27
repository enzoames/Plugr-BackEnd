from rest_framework import serializers
from photologue.models import Photo
from .models import *


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class EnzoGallerySerializer(serializers.ModelSerializer):
	# many=True: since Photo object has no nested intems then you dont need many=true
	photo = PhotoSerializer()

	class Meta:
		model = EnzoGallery
		fields = '__all__'


class ContactEnzoAmesSerializer(serializers.ModelSerializer):
	class Meta:
		model = ContactEnzoAmes
		fields = '__all__'

	def create(self, validate_data):
		data = validate_data
		print("\nDATA:", data)
		#print(json.dumps(data, indent=4))
		register = ContactEnzoAmes.objects.create(**data)
		return register
