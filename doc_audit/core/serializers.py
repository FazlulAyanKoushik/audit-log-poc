from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Document, DocumentAccess
from auditlog.context import set_actor


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class DocumentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ["id", "title", "content", "owner", "created_at", "updated_at"]
        read_only_fields = ["owner", "created_at", "updated_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        # create instance without saving
        doc = Document(owner=user, **validated_data)
        with set_actor(user):
            doc.save()
        return doc

    def update(self, instance, validated_data):
        user = self.context["request"].user
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        with set_actor(user):
            instance.save()
        return instance


class DocumentAccessSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="user"
    )

    class Meta:
        model = DocumentAccess
        fields = ["id", "document", "user", "user_id", "access_type"]
        read_only_fields = ["document"]


    def create(self, validated_data):
        document = validated_data.pop("document")
        user = validated_data.pop("user")
        user_id = validated_data.pop("user_id")
        access_type = validated_data.pop("access_type")
        return DocumentAccess.objects.create(document=document, user=user_id, access_type=access_type)

    def update(self, instance, validated_data):
        instance.access_type = validated_data.get("access_type", instance.access_type)
        instance.save()
        return instance




# ====================================Document History==============================================
from auditlog.models import LogEntry


class LogEntrySerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)

    class Meta:
        model = LogEntry
        fields = ["id", "actor", "action", "changes", "timestamp"]

