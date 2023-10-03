# Generated by Django 4.2.5 on 2023-10-03 06:47

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_events_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventname', models.CharField(max_length=100)),
                ('teamname', models.CharField(max_length=200)),
                ('teammates', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('password', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('eventstatus', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=8)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
        ),
    ]
