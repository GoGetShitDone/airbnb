from django.http import JsonResponse
from django.core import serializers
from .models import Category


def categories(request):
    all_categories = Category.objects.all()
    return JsonResponse({"ok": True, "categories": serializers.serialize("json", all_categories), })
