from rest_framework import serializers


class LinkTelegramSerializer(serializers.Serializer):
    tg_username = serializers.CharField(required=False, allow_blank=True)
    tg_chat_id = serializers.IntegerField(required=True)
