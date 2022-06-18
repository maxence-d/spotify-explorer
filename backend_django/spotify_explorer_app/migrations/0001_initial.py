# Generated by Django 4.0.5 on 2022-06-18 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sp_id', models.CharField(max_length=255)),
                ('followers', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]