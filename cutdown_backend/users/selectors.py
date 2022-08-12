from typing import Union

from .models import CustomUser


def get_user_by_email(email: str) -> Union[None, CustomUser]:
    return CustomUser.objects.filter(email=email).first()
