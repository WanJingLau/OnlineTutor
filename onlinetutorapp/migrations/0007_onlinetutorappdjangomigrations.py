# Generated by Django 4.0.2 on 2022-02-23 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinetutorapp', '0006_captchacaptchastore_postofficeattachment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlinetutorappDjangomigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'onlinetutorapp_djangomigrations',
                'managed': False,
            },
        ),
    ]
