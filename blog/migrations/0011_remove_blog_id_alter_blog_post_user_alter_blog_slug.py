# Generated by Django 4.1.5 on 2023-01-03 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0010_blog_id_alter_blog_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='id',
        ),
        migrations.AlterField(
            model_name='blog',
            name='post_user',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(primary_key=True, serialize=False),
        ),
    ]
