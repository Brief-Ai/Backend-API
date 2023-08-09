# Generated by Django 4.2.3 on 2023-08-08 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_remove_search_user_search_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=255)),
                ('interests', models.TextField(blank=True)),
            ],
        ),
    ]