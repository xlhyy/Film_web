from django.db import models

class FilmInfo(models.Model):
    m_id = models.AutoField(primary_key=True)
    names = models.CharField(max_length=255, blank=True, null=True)
    posters = models.CharField(max_length=100, blank=True, null=True)
    grades = models.CharField(max_length=100, blank=True, null=True)
    directors = models.CharField(max_length=255, blank=True, null=True)
    writers = models.CharField(max_length=500, blank=True, null=True)
    actors = models.CharField(max_length=1000, blank=True, null=True)
    types = models.CharField(max_length=255, blank=True, null=True)
    countrys = models.CharField(max_length=255, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    show_times = models.CharField(max_length=255, blank=True, null=True)
    run_times = models.CharField(max_length=255, blank=True, null=True)
    intros = models.CharField(max_length=255, blank=True, null=True)
    contents = models.CharField(max_length=1000, blank=True, null=True)
    youku_urls = models.CharField(db_column='YouKu_urls', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tengxun_urls = models.CharField(db_column='TengXun_urls', max_length=255, blank=True, null=True)  # Field name made lowercase.
    souhu_urls = models.CharField(db_column='SouHu_urls', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aiqiyi_urls = models.CharField(db_column='AiQiYi_urls', max_length=255, blank=True, null=True)  # Field name made lowercase.

class UserInfo(models.Model):
    username = models.CharField(max_length=255)
    u_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255)

class CollectInfo(models.Model):
    c_id = models.AutoField(primary_key=True)
    film_name = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)

class ZanOrCaiInfo(models.Model):
    film_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    z_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255)

class CommentInfo(models.Model):
    user_name = models.CharField(max_length=255)
    film_name = models.CharField(max_length=255)
    comment_text = models.CharField(max_length=1000)
    comment_time = models.CharField(max_length=255)
    com_id = models.AutoField(primary_key=True)

class BarrageInfo(models.Model):
    b_id = models.AutoField(primary_key=True)
    time_count = models.CharField(max_length=255)
    barrage_text = models.CharField(max_length=255)
    film_name = models.CharField(max_length=255)