from rest_framework import status
from rest_framework.test import APITestCase

from .models import Ticket


class TicketCreateValidationTest(APITestCase):
    def test_cannot_create_ticket_with_closed_status(self):
        response = self.client.post(
            "/api/tickets/",
            {"title": "Test ticket", "status": "closed"},
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

    def test_closed_to_open_fails(self):
        response = self.client.patch(
            f"/api/tickets/{self.ticket.id}/",
            {"status": "open"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.CLOSED)

    def test_closed_to_in_progress_succeeds(self):
        response = self.client.patch(
            f"/api/tickets/{self.ticket.id}/",
            {"status": "in_progress"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.IN_PROGRESS)


class TicketStatsTest(APITestCase):
    def test_stats_returns_correct_counts(self):
        Ticket.objects.create(title="T1", status="open")
        Ticket.objects.create(title="T2", status="open")
        Ticket.objects.create(title="T3", status="closed")

        response = self.client.get("/api/tickets/stats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {item["status"]: item["total"] for item in response.data}
        self.assertEqual(data["open"], 2)
        self.assertEqual(data["closed"], 1)
        self.assertNotIn("in_progress", data)
