# Generated by Django 4.0.2 on 2022-02-06 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_rename_describtion_word_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='synonyms',
            field=models.ManyToManyField(blank=True, to='content.Word'),
        ),
    ]
