from typing import Any

from django import template


register = template.Library()


@register.filter
def subtract(value: Any, arg: Any) -> Any:
    """
    Шаблонный фильтр - вычитание.
    """
    return value - arg
