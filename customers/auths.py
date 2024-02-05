from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                Q(email__iexact=email) | Q(email__iexact=email)
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = (
                UserModel.objects.filter(
                    Q(email__iexact=email) | Q(email__iexact=email)
                )
                .order_by("id")
                .first()
            )

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
