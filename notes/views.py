from rest_framework import generics, status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Note
from .permissions import IsOwnerOrAdmin
from .serializers import NoteSerializer

class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["created_at", "updated_at", "title"]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user():
            return Note.objects.select_related("owner").all()
        return Note.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user():
            return Note.objects.select_related("owner").all()
        return Note.objects.filter(owner=user)

    def update(self, request, *args, **kwargs):
        note = self.get_object()
        if request.user.is_admin_user() and note.owner != request.user:
            raise PermissionDenied("Admins can view and delete notes, but not edit others' notes.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        note = self.get_object()
        note.delete()
        return Response({"message": "Note deleted successfully."}, status=status.HTTP_200_OK)