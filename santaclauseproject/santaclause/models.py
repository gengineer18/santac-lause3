from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    """ユーザープロフィール"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    introduce = models.CharField(max_length=400, blank=True)
    location = models.CharField(max_length=30, blank=True)
    web_site = models.CharField(max_length=2100, blank=True)
    icon = models.ImageField(upload_to="user/image", blank=True)

    class Meta:
        db_table = 'profile'

    def save(self, *args, **kwargs):  # 変更アイコン画像の削除処理
        try:
            original_icon = Profile.objects.get(pk=self.pk)
            if original_icon.icon != self.icon:  # 画像に変更があれば過去分は削除する
                original_icon.icon.delete(save=False)
        except self.DoesNotExist:
            pass

        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Present(models.Model):
    """投稿"""
    # user_id = models.IntegerField('ユーザーID')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=80)
    conclusion = models.CharField('まとめると', max_length=400)
    topic1 = models.CharField('トピック1', max_length=140)
    image1 = models.ImageField('画像1', upload_to="present/image", blank=True)
    contents1 = models.CharField('コンテンツ1', max_length=1024)
    topic2 = models.CharField('トピック2', max_length=140)
    image2 = models.ImageField('画像2', upload_to="present/image", blank=True)
    contents2 = models.CharField('コンテンツ2', max_length=1024)
    topic3 = models.CharField('トピック3', max_length=140)
    image3 = models.ImageField('画像3', upload_to="present/image", blank=True)
    contents3 = models.CharField('コンテンツ3', max_length=1024)
    favorite = models.IntegerField('お気に入り', default=0)
    create_date = models.DateField('作成日', default=timezone.now)
    update_date = models.DateField('更新日', default=timezone.now)

    class Meta:
        db_table = 'present'

    def save(self, *args, **kwargs):  # 画像の差し替え時の旧画像削除処理
        try:
            original_image = Present.objects.get(pk=self.pk)
            if original_image.image1 != self.image1:
                original_image.image1.delete(save=False)
            if original_image.image2 != self.image2:
                original_image.image2.delete(save=False)
            if original_image.image3 != self.image3:
                original_image.image3.delete(save=False)
        except self.DoesNotExist:
            pass

        super(Present, self).save(*args, **kwargs)
