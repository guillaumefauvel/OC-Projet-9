# Generated by Django 4.0.1 on 2022-01-31 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_ticket_ticket_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
