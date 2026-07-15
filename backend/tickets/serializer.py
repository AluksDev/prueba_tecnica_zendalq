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
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_status(self, value):
        if self.instance is None and value == Ticket.Status.CLOSED:
            raise serializers.ValidationError(
                "New tickets cannot start closed."
            )
        return value

    def validate(self, data):
        if self.instance:
            old_status = self.instance.status
            new_status = data.get("status", old_status)
            if old_status == Ticket.Status.CLOSED and new_status == Ticket.Status.OPEN:
                raise serializers.ValidationError(
                    {
                        "status": "Closed tickets cannot be reopened."
                    }
                )
        return data
