from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from users.models import User
from .services import send_telegram_message


class LinkTelegramView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        chat_id = request.data.get("chat_id")
        username = request.data.get("username")  # опционально

        if not chat_id:
            return Response(
                {"detail": "chat_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user: User = request.user
        user.tg_chat_id = chat_id
        if username:
            user.tg_username = username
        user.save(
            update_fields=["tg_chat_id", "tg_username"] if username else ["tg_chat_id"]
        )

        # пробное сообщение, можно убрать
        try:
            send_telegram_message(chat_id, "Готово! Аккаунт привязан ✅")
        except Exception as e:
            # не валим запрос, просто сообщаем
            return Response(
                {"status": "linked", "warn": f"TG send failed: {e}"},
                status=status.HTTP_200_OK,
            )

        return Response({"status": "linked"}, status=status.HTTP_200_OK)
