# Generated by Django 4.1.5 on 2023-01-03 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_blog_tag'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Blog',
        ),
    ]
