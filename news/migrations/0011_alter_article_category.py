# Generated by Django 4.2.3 on 2023-08-09 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_alter_article_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
