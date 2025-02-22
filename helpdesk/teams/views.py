from __future__ import annotations

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import CharField, F, QuerySet, Value
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from helpdesk.forms import CommentSubmitForm
from tickets.filters import TeamTicketFilter
from tickets.models import Ticket, TicketComment, TicketResolution
from tickets.tables import TicketTable

from .filters import TeamFilterset
from .models import Team, TeamComment
from .tables import TeamTable


class TicketDetailRedirectView(RedirectView):

    pattern_name = "teams:team_detail_tickets"


class TeamListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Team
    table_class = TeamTable
    filterset_class = TeamFilterset

class TeamDetailAboutView(LoginRequiredMixin, DetailView):

    model = Team
    slug_field = "tla"
    template_name_suffix = "_detail_about"

class TeamDetailCommentsView(LoginRequiredMixin, DetailView):

    model = Team
    slug_field = "tla"
    template_name_suffix = "_detail_comments"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        return super().get_context_data(
            comment_form=CommentSubmitForm(),
            **kwargs,
        )
    
class TeamSubmitCommentFormView(LoginRequiredMixin, FormMixin, SingleObjectMixin, ProcessFormView):

    http_method_names = ['post', 'put']
    model = Team
    slug_field = "tla"
    form_class = CommentSubmitForm

    def get_success_url(self) -> str:
        return reverse_lazy('teams:team_detail_comments', kwargs={"slug": self.get_object().tla})

    def form_valid(self, form: CommentSubmitForm) -> HttpResponse:
        assert self.request.user.is_authenticated
        team = self.get_object()
        team.comments.create(
            content=form.cleaned_data['comment'],
            author=self.request.user,
        )
        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def form_invalid(self, form: CommentSubmitForm) -> HttpResponse:
        return HttpResponse("Please fill out the form correctly.")


class TeamDetailTicketsView(LoginRequiredMixin, SingleTableMixin, DetailView):
    model = Team
    slug_field = "tla"
    table_class = TicketTable
    template_name_suffix = "_detail_tickets"

    def get_ticket_queryset(self) -> QuerySet[Ticket]:
        return self.get_object().tickets.all()
    
    def get_ticket_filter(self) -> TeamTicketFilter:
        queryset = self.get_ticket_queryset()
        
        return TeamTicketFilter(
            data=self.request.GET or None,
            request=self.request,
            queryset=queryset,
            initial_resolution=None,
        )

    def get_table_data(self) -> QuerySet[Ticket]:
        data_filter = self.get_ticket_filter()
        return data_filter.qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["filter"] = self.get_ticket_filter()
        return context


class TeamDetailTimelineView(LoginRequiredMixin, DetailView):

    model = Team
    slug_field = "tla"
    template_name_suffix = "_detail_timeline"

    def get_entries(self) -> QuerySet[Any]:
        fields = ("entry_type", "entry_timestamp", "entry_user", "entry_content", "entry_style_info")

        tickets = Ticket.objects.filter(team=self.object).order_by().annotate(
            entry_type=Value('Ticket Opened ', output_field=CharField()),
            entry_timestamp=F("created_at"),
            entry_user=F("opened_by"),
            entry_content=F("description"),
            entry_style_info=Value('is-info', output_field=CharField()),
        ).values(*fields)

        comments = TicketComment.objects.filter(ticket__team=self.object).order_by().annotate(
            entry_type=Value('Ticket Comment', output_field=CharField()),
            entry_timestamp=F("created_at"),
            entry_user=F("author"),
            entry_content=F("content"),
            entry_style_info=Value('', output_field=CharField()),
        ).values(*fields)

        resolutions = TicketResolution.objects.filter(ticket__team=self.object).order_by().annotate(
            entry_type=Value('Ticket Resolution', output_field=CharField()),
            entry_timestamp=F("resolved_at"),
            entry_user=F("user"),
            entry_content=F("comment"),
            entry_style_info=Value('is-success', output_field=CharField()),
        ).values(*fields)

        team_comments = TeamComment.objects.filter(team=self.object).order_by().annotate(
            entry_type=Value('Team Comment', output_field=CharField()),
            entry_timestamp=F("created_at"),
            entry_user=F("author"),
            entry_content=F("content"),
            entry_style_info=Value('', output_field=CharField()),
        ).values(*fields)

        return comments.union(resolutions, tickets, team_comments).order_by("-entry_timestamp")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(entries=self.get_entries(), **kwargs)
