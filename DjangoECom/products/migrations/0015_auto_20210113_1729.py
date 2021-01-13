# Generated by Django 3.1.4 on 2021-01-13 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_merge_20210111_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Clothes', 'Clothes'), ('Mobiles', 'Mobiles'), ('TVs', 'TVs'), ('VideoGamesAndConsols', 'VideoGamesAndConsols'), ('PC', 'PC')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='empty_img.png', null=True, upload_to='media/'),
        ),
    ]
