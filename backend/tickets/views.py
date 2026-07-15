from django.db.models import Count

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ticket
from .serializer import TicketSerializer


class TicketViewSet(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    @action(
        detail=False,
        methods=["get"]
    )
    def stats(self, request):
        stats = (
            self.get_queryset()
            .values("status")
            .annotate(total=Count("id"))
        )

        return Response(stats)