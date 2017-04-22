from rest_framework import serializers

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    platform_type = serializers.CharField()
    token_type = serializers.CharField()
