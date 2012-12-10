from django.db import models
from django.utils.translation import ugettext as _


class Category(models.Model):

    title = models.CharField(max_length=50)
    slug = models.SlugField()
    order = models.IntegerField(default=1)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order']

    def __unicode__(self):
        return self.title


class WMSServer(models.Model):

    title = models.CharField(max_length=50)
    url = models.URLField()
    attribution = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('WMSServer')
        verbose_name_plural = _('WMSServers')

    def __unicode__(self):
        return self.title
    

class Layer(models.Model):

    WMS_FORMAT_OPTIONS = (
        ('image/png', 'image/png'),
        ('image/jpeg', 'image/jpeg'),
    )

    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    visible = models.BooleanField()
    category_order = models.IntegerField(default=1)
    map_order = models.IntegerField(default=1)

    wms_server = models.ForeignKey(WMSServer)
    wms_layers = models.CharField(max_length=100)
    wms_styles = models.CharField(max_length=100, null=True, blank=True)
    wms_format = models.CharField(max_length=10, choices=WMS_FORMAT_OPTIONS, default='image/png')
    wms_transparent = models.BooleanField(default=True)


    class Meta:
        verbose_name = _('Layer')
        verbose_name_plural = _('Layers')
        ordering = ['category_order']

    def __unicode__(self):
        return self.title
