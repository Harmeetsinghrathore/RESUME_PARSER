from rest_framework import serializers
from .models import Resume_Data, Resume_file


class FileSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source = 'user.id')
    class Meta:
        model = Resume_file
        fields = '__all__'

class ResumeDataSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source = 'user.id')
    class Meta:
        model = Resume_Data
        fields = '__all__'