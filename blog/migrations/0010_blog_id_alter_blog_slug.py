# Generated by Django 4.1.5 on 2023-01-03 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_remove_blog_id_alter_blog_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(),
        ),
    ]
