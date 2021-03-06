# Generated by Django 3.0.5 on 2022-01-28 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('access_register', '0003_auto_20220126_2305'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoggerUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('ip_user', models.TextField(default='0.0.0.0')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sequenzaLogUser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Utente_log',
                'verbose_name_plural': 'Utenti_log',
            },
        ),
    ]
