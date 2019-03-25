from rest_framework import serializers
from bori.models import RcmdNews
from django.contrib.auth.models import User

class RcmdNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RcmdNews
        fields = "__all__"
