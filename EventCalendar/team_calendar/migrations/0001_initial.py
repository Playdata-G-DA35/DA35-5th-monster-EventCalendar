# Generated by Django 5.0.6 on 2024-07-04 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CalenderData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=50)),
                ('scheduled_date', models.DateField()),
                ('scheduled_member', models.CharField(max_length=50)),
                ('scheduled_for', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=50)),
                ('team_manager', models.CharField(max_length=50)),
                ('member1', models.CharField(max_length=50)),
                ('member2', models.CharField(max_length=50)),
                ('member3', models.CharField(max_length=50)),
            ],
        ),
    ]
