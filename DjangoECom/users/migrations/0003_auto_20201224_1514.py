# Generated by Django 3.1.4 on 2020-12-24 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201221_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(default='profile_pic.png', upload_to=''),
        ),
    ]
