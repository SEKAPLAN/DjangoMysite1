# Generated by Django 3.0.4 on 2020-06-17 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_content_price'),
        ('order', '0003_auto_20200616_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduce',
            name='content',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='content.Content'),
            preserve_default=False,
        ),
    ]
