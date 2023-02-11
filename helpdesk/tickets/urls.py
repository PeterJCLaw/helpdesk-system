from django.urls import path

from .views import (
    AssignedTicketListView,
    RedirectToDefaultTicketQueue,
    TicketDetailView,
    TicketQueueDetailView,
    TicketResolveFormView,
    TicketSubmitCommentFormView,
)

app_name = "tickets"

urlpatterns = [
    path("", RedirectToDefaultTicketQueue.as_view(), name="queue_default"),
    path(
        "assigned-to-me", AssignedTicketListView.as_view(), name="ticket_assigned_list"
    ),
    path("<slug:slug>", TicketQueueDetailView.as_view(), name="queue_detail"),
    path("ticket/<int:pk>", TicketDetailView.as_view(), name="ticket_detail"),
    path("ticket/<int:pk>/comment", TicketSubmitCommentFormView.as_view(), name="ticket_comment"),
    path("ticket/<int:pk>/resolve", TicketResolveFormView.as_view(), name="ticket_resolve"),
]
