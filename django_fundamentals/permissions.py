"""*the 4-tier authorization model: Anonymous / Authenticated / Staff / Superuser*

1. Anonymous — Django's built-in ``AnonymousUser``, read-only access to
   public content.
2. Authenticated — ``is_active=True`` plus Groups/Permissions; can
   create/edit/delete their own content only.
3. Staff — ``is_staff=True`` (Django admin access).
4. Superuser — ``is_superuser=True`` (bypasses all permission checks).
"""

from django.contrib.auth.mixins import UserPassesTestMixin
from guardian.shortcuts import assign_perm
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """*DRF permission: tier 2 — authenticated users may write only to objects they own*

    Expects the target object to expose an ``owner`` attribute.

    **Usage:**

    ```python
    class WidgetViewSet(viewsets.ModelViewSet):
        permission_classes = [IsOwnerOrReadOnly]
    ```
    """

    def has_object_permission(self, request, view, targetObject):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(targetObject, "owner_id", None) == request.user.id


class IsStaffUser(permissions.BasePermission):
    """*DRF permission: tier 3 — requires ``is_staff``*"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsSuperUser(permissions.BasePermission):
    """*DRF permission: tier 4 — requires ``is_superuser``*"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class StaffRequiredMixin(UserPassesTestMixin):
    """*Django view mixin: tier 3 — requires ``is_staff`` to access a view*"""

    def test_func(self):
        return bool(self.request.user.is_authenticated and self.request.user.is_staff)


class SuperuserRequiredMixin(UserPassesTestMixin):
    """*Django view mixin: tier 4 — requires ``is_superuser`` to access a view*"""

    def test_func(self):
        return bool(self.request.user.is_authenticated and self.request.user.is_superuser)


def assign_owner_permissions(user, targetObject):
    """*grant a tier-2 authenticated user guardian object-level view/change/delete permissions over an object they just created*

    **Key Arguments:**

    - ``user`` -- the owning user
    - ``targetObject`` -- the model instance to grant permissions over

    **Usage:**

    ```python
    widget = Widget.objects.create(owner=request.user, name="thing")
    assign_owner_permissions(request.user, widget)
    ```
    """
    modelName = targetObject._meta.model_name
    for action in ("view", "change", "delete"):
        assign_perm(f"{action}_{modelName}", user, targetObject)
