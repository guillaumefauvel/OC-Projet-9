# Generated by Django 4.0.1 on 2022-02-16 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='headline',
            field=models.CharField(max_length=32, verbose_name='Titre'),
        ),
    ]