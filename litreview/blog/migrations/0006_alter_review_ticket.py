# Generated by Django 4.0.1 on 2022-01-31 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.ticket'),
        ),
    ]