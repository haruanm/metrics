from django.db import models

# Create your models here.
class File(models.Model):
    age_days = models.FloatField()
    comments = models.IntegerField()
    absolute_path = models.TextField()
    filename = models.CharField(max_length=255)
    mccabe = models.IntegerField()
    committers_count = models.IntegerField()
    change_frequency = models.IntegerField()
    ratio_comment_to_code = models.FloatField()
    sloc = models.IntegerField()
    language = models.CharField(max_length=255)
    relative_path = models.TextField()

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"


class FileDependsOnFile(models.Model):
    origin = models.ForeignKey(File, on_delete=models.DO_NOTHING)
    depends_on = models.ForeignKey(File, on_delete=models.DO_NOTHING, related_name="file_depends_on_destionations")

    class Meta:
        verbose_name = "FileDependsOnFile"
        verbose_name_plural = "FileDependsOnFiles"

    def __unicode__(self):
        pass


class Function(models.Model):
    file = models.ForeignKey(File, on_delete=models.DO_NOTHING)
    name = models.TextField()
    start = models.IntegerField()
    function_path = models.TextField()
    end = models.IntegerField()


class Class(models.Model):
    file = models.ForeignKey(File, on_delete=models.DO_NOTHING)
    name = models.TextField()
    start = models.IntegerField()
    class_path = models.TextField()
    end = models.IntegerField()

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classs"

    def __unicode__(self):
        pass


class Method(models.Model):
    _class = models.ForeignKey(Class, on_delete=models.DO_NOTHING)
    name = models.TextField()
    start = models.IntegerField()
    end = models.IntegerField()
    method_path = models.TextField()

    class Meta:
        verbose_name = "Method"
        verbose_name_plural = "Methods"

    def __unicode__(self):
        pass
