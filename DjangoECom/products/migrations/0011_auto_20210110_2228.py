# Generated by Django 3.1.4 on 2021-01-10 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20210110_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Clothes', 'Clothes'), ('Mobiles', 'Mobiles'), ('TVs', 'TVs'), ('Video games and Consols', 'Video games and Consols'), ('PC', 'PC')], max_length=50, null=True),
        ),
    ]
