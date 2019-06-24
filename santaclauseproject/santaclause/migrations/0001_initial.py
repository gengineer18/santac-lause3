# Generated by Django 2.1.7 on 2019-06-23 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Present',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='タイトル')),
                ('conclusion', models.CharField(max_length=400, verbose_name='まとめると')),
                ('topic1', models.CharField(max_length=140, verbose_name='トピック1')),
                ('image1', models.ImageField(blank=True, upload_to='present/image', verbose_name='画像1')),
                ('contents1', models.CharField(max_length=1024, verbose_name='コンテンツ1')),
                ('topic2', models.CharField(max_length=140, verbose_name='トピック2')),
                ('image2', models.ImageField(blank=True, upload_to='present/image', verbose_name='画像2')),
                ('contents2', models.CharField(max_length=1024, verbose_name='コンテンツ2')),
                ('topic3', models.CharField(max_length=140, verbose_name='トピック3')),
                ('image3', models.ImageField(blank=True, upload_to='present/image', verbose_name='画像3')),
                ('contents3', models.CharField(max_length=1024, verbose_name='コンテンツ3')),
                ('favorite', models.IntegerField(default=0, verbose_name='お気に入り')),
                ('create_date', models.DateField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('update_date', models.DateField(default=django.utils.timezone.now, verbose_name='更新日')),
            ],
            options={
                'db_table': 'present',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('introduce', models.CharField(blank=True, max_length=400)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('web_site', models.CharField(blank=True, max_length=2100)),
                ('icon', models.ImageField(blank=True, upload_to='user/image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profile',
            },
        ),
        migrations.AddField(
            model_name='present',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='santaclause.Profile'),
        ),
    ]
