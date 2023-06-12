from rest_framework.serializers import *
from .models import *

class item_serializer(ModelSerializer):
    class Meta:
        model = item
        fields = '__all__'

class cart_serializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'