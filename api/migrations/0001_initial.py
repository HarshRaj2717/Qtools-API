# Generated by Django 4.2.1 on 2023-07-14 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=65)),
                ('api_token', models.CharField(max_length=65)),
                ('verified', models.BooleanField(default=False)),
                ('cur_code', models.CharField(max_length=65)),
                ('active', models.BooleanField(default=True)),
                ('tier', models.PositiveSmallIntegerField(default=0)),
                ('files_transferred_mb', models.PositiveIntegerField(default=0)),
                ('api_calls_count', models.PositiveIntegerField(default=0)),
                ('last_api_call_month', models.DateField(auto_now=True)),
            ],
        ),
    ]
