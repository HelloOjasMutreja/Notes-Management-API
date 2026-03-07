from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Note
        fields = ["id", "title", "content", "owner_username", "created_at", "updated_at"]
        read_only_fields = ["id", "owner_username", "created_at", "updated_at"]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be blank.")
        return value.strip()

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be blank.")
        return value.strip()