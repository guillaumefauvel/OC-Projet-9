# Generated by Django 4.0.1 on 2022-01-31 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_review_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]