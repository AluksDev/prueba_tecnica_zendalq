from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Ticket


class TicketCreateValidationTest(APITestCase):
    def test_cannot_create_ticket_with_closed_status(self):
        url = reverse("ticket-list")

        response = self.client.post(
            url,
            {
                "title": "Test ticket",
                "status": Ticket.Status.CLOSED,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            Ticket.objects.filter(title="Test ticket").exists()
        )


class TicketTransitionValidationTest(APITestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            title="Closed ticket",
            status=Ticket.Status.CLOSED,
        )
        self.url = reverse(
            "ticket-detail",
            kwargs={"pk": self.ticket.id},
        )

    def test_closed_ticket_cannot_transition_directly_to_open(self):
        response = self.client.patch(
            self.url,
            {"status": Ticket.Status.OPEN},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.ticket.refresh_from_db()
        self.assertEqual(
            self.ticket.status,
            Ticket.Status.CLOSED,
        )

    def test_closed_ticket_can_transition_to_in_progress(self):
        response = self.client.patch(
            self.url,
            {"status": Ticket.Status.IN_PROGRESS},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.ticket.refresh_from_db()
        self.assertEqual(
            self.ticket.status,
            Ticket.Status.IN_PROGRESS,
        )


class TicketStatsTest(APITestCase):
    def test_stats_returns_correct_ticket_counts_by_status(self):
        Ticket.objects.create(
            title="Open ticket 1",
            status=Ticket.Status.OPEN,
        )
        Ticket.objects.create(
            title="Open ticket 2",
            status=Ticket.Status.OPEN,
        )
        Ticket.objects.create(
            title="Closed ticket",
            status=Ticket.Status.CLOSED,
        )

        url = reverse("ticket-stats")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            item["status"]: item["total"]
            for item in response.data
        }

        self.assertEqual(data[Ticket.Status.OPEN], 2)
        self.assertEqual(data[Ticket.Status.CLOSED], 1)