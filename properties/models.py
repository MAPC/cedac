from django.contrib.gis.db import models
from django.utils.translation import ugettext as _


# south introspection rules
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.PointField'])
except ImportError:
    pass


class ExpUse(models.Model):

    propertyid = models.IntegerField(primary_key=True)
    hudid = models.IntegerField('HUDID', null=True, blank=True)
    property_name_text = models.CharField(max_length=50, null=True, blank=True)
    address_line1_text = models.CharField(max_length=50, null=True, blank=True)
    city_name_text = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    # property_total_unit_count = models.IntegerField()
    units_elderly_c = models.IntegerField(null=True, blank=True)
    units_0br_c = models.IntegerField(null=True, blank=True)
    units_1br_c = models.IntegerField(null=True, blank=True)
    units_2br_c = models.IntegerField(null=True, blank=True)
    units_3br_c = models.IntegerField(null=True, blank=True)
    units_4mbr_c = models.IntegerField(null=True, blank=True)
    units_assisted = models.IntegerField(null=True, blank=True)
    project_aka = models.CharField(max_length=200, null=True, blank=True)
    units_at_risk_num_2015 = models.IntegerField(null=True, blank=True)
    units_at_risk_num_2020 = models.IntegerField(null=True, blank=True)
    units_at_risk_num_2025 = models.IntegerField(null=True, blank=True)

    # temporary for import and geocoding
    lon = models.FloatField()
    lat = models.FloatField()

    geometry = models.PointField(geography=True, null=True, blank=True)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Expiring Use Property')
        verbose_name_plural = _('Expiring Use Properties')

    def __unicode__(self):
        return self.property_name_text

    def aka_title(self):
        if self.project_aka != None:
            return self.project_aka.title()

    def address(self):
        return '%s, %s, MA %s' % (self.address_line1_text.title(), self.city_name_text.title(), self.zip_code)

