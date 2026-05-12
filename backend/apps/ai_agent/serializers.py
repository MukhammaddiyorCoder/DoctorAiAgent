from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    clinic_slug = serializers.SlugField()
    session_key = serializers.CharField(max_length=64)
    message = serializers.CharField()


class ChatResponseSerializer(serializers.Serializer):
    reply = serializers.CharField()
