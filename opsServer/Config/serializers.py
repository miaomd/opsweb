from rest_framework import serializers
from .models import menu, WebAuth, UserAuth

class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        fields = ["id", "mid", "username","m_path", "switch", "state"]


class WebAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebAuth
        fields = ["id", "mid", "role","m_path", "switch", "state"]


class WebMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = menu
        fields = ["id", "path", "redirect", "meta_title",  "meta_icon","meta_cache","alway_show", 
                  "hideClose", "component", "fid", "step","index","has_child","state"]

