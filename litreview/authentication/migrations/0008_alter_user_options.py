# Generated by Django 4.0.1 on 2022-02-10 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_user_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-username']},
        ),
    ]
