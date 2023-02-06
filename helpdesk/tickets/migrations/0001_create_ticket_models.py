# Generated by Django 3.2.17 on 2023-02-06 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_create_team_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Ticket Queue Name')),
                ('slug', models.SlugField(max_length=32, verbose_name='Slug')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('status', models.CharField(choices=[('OP', 'Open'), ('AR', 'Awaiting Team Response'), ('BL', 'Blocked'), ('CL', 'Closed')], default='OP', max_length=2)),
                ('priority', models.CharField(choices=[('L', 'Low'), ('N', 'Normal'), ('H', 'High')], default='N', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tickets', related_query_name='tickets', to=settings.AUTH_USER_MODEL)),
                ('opened_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', related_query_name='tickets', to='tickets.ticketqueue')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', related_query_name='tickets', to='teams.team')),
            ],
        ),
    ]
