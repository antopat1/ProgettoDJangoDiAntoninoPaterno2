# Generated by Django 3.0.5 on 2022-02-20 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access_register', '0008_search_iduser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Count_words_onItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sWord', models.CharField(max_length=26)),
            ],
        ),
    ]
