# Generated by Django 3.0.6 on 2020-05-25 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0003_auto_20200525_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='location',
        ),
        migrations.AddField(
            model_name='company',
            name='locations',
            field=models.ManyToManyField(related_name='companies', to='landing_page.Location'),
        ),
    ]
