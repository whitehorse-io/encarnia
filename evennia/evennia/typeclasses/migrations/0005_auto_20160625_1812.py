# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 18:12
from __future__ import unicode_literals

from django.db import migrations

# Migration of old nick format to new

def update_nicks(apps, schema_editor):
    Attribute = apps.get_model("typeclasses", "Attribute")
    for nick in Attribute.objects.filter(db_attrtype="nick"):
        try:
            _, _, _, _ = nick.db_value
        except (TypeError, ValueError):
            # old setup, we store it in the new format - old uses its own key
            # as regex to keep the old matching (and has no $-type args)
            nick.db_value = (nick.db_key, nick.db_strvalue, nick.db_key, nick.db_strvalue)
            nick.save()


class Migration(migrations.Migration):

    dependencies = [
        ('typeclasses', '0004_auto_20151101_1759'),
    ]

    operations = [
        migrations.RunPython(update_nicks)
    ]
