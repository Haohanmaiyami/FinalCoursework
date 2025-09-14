from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Личный список доступен только аутентифицированному
        if request.method in SAFE_METHODS:
            if getattr(view, "action", None) == "list":
                return bool(request.user and request.user.is_authenticated)
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # SAFE: читать можно публичное или своё
        if request.method in SAFE_METHODS:
            return bool(
                obj.is_public or (getattr(request.user, "id", None) == obj.user_id)
            )
        # write: только владелец
        return getattr(request.user, "id", None) == obj.user_id
