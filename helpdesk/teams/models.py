from __future__ import annotations

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse_lazy


class Team(models.Model):
    tla = models.CharField(
        "TLA",
        max_length=4,
        unique=True,
        validators=[
            RegexValidator(r"^[A-Z]{3}\d*$", "Must match TLA format."),
        ],
    )
    name = models.CharField("Team Name", max_length=100)
    is_rookie = models.BooleanField("Is Rookie")

    def __str__(self) -> str:
        return f"{self.tla} - {self.name}"

    def get_absolute_url(self) -> str:
        return reverse_lazy('teams:team_detail', kwargs={'tla': self.tla})
