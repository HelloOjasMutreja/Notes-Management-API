from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "owner", "created_at", "updated_at"]
    list_filter = ["owner"]
    search_fields = ["title", "content", "owner__username"]
    readonly_fields = ["created_at", "updated_at"]