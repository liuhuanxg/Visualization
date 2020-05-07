from django.db import models


# 经纬度信息表
class LongitudeLatitude(models.Model):
    class Meta:
        verbose_name = "经纬度"
        verbose_name_plural = "经纬度"

    longitude = models.CharField(max_length=10,verbose_name="经度")
    latitude = models.CharField(max_length=10,verbose_name="纬度")


# 地质数据表
class Geology(models.Model):
    class Meta:
        verbose_name = "地质"
        verbose_name_plural = "地质"

    geology_name = models.CharField(verbose_name="地质类别", max_length=10, unique=True)
    number = models.IntegerField("编号")

    def __str__(self):
        return self.geology_name

    def __repr__(self):
        return self.geology_name


# 地理信息表
class Geographic_Information(models.Model):
    class Meta:
        verbose_name = "地理信息"
        verbose_name_plural = "地理信息"
    geology = models.ForeignKey("Geology", on_delete=models.CASCADE)
    longitudelatitude = models.ForeignKey("LongitudeLatitude", on_delete=models.CASCADE)
    depth = models.IntegerField(verbose_name="深度")


