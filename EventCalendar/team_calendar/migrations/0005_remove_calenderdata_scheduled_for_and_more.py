# Generated by Django 5.0.6 on 2024-07-05 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_calendar', '0004_alter_team_member1_alter_team_member2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calenderdata',
            name='scheduled_for',
        ),
        migrations.AddField(
            model_name='calenderdata',
            name='scheduled_end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='calenderdata',
            name='scheduled_month',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='calenderdata',
            name='scheduled_start_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='calenderdata',
            name='scheduled_year',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='calenderdata',
            name='scheduled_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='calenderdata',
            name='scheduled_member',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
