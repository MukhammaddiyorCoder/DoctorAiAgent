from rest_framework import permissions


class IsClinicOwner(permissions.BasePermission):
    """
    Allows access only to authenticated users who own a clinic.
    Object-level permission compares `obj.clinic.owner` with request.user.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        owner = getattr(getattr(obj, "clinic", None), "owner", None)
        return owner == request.user
