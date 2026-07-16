from rest_framework import serializers

from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_status(self, value):
        if self.instance is None and value == Ticket.Status.CLOSED:
            raise serializers.ValidationError(
                "No se puede crear un ticket con estado cerrado."
            )
        return value

    def validate(self, data):
        if self.instance:
            old_status = self.instance.status
            new_status = data.get("status", old_status)
            if old_status == Ticket.Status.CLOSED and new_status == Ticket.Status.OPEN:
                raise serializers.ValidationError(
                    {
                        "status": "Un ticket cerrado no puede volver a abierto directamente."
                    }
                )
        return data
