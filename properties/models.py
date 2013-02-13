from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from django.contrib.gis.geos import Point

from pygeocoder import Geocoder


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
    property_total_unit_count = models.IntegerField(null=True, blank=True)
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
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)

    # geocoding results
    geocoded = models.BooleanField()
    geocoded_address = models.CharField(max_length=200, null=True)

    geometry = models.PointField(geography=True, null=True, blank=True)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Expiring Use Property')
        verbose_name_plural = _('Expiring Use Properties')

    def __unicode__(self):
        return self.property_name_text

    @property
    def aka_title(self):
        if self.project_aka != None:
            return self.project_aka.title()

    @property
    def address(self):
        return '%s, %s, MA %s' % (self.address_line1_text.title(), self.city_name_text.title(), self.zip_code)

    def save(self, *args, **kwargs):

        # compare new with previously saved object
        # and decide if we need to geocode or not
        if ExpUse.objects.filter(pk=self.pk).exists():
            prev_obj = ExpUse.objects.get(pk=self.pk)
            self.geocoded = prev_obj.geocoded
            # address changed, geocode
            if self.address <> prev_obj.address:
                self.geocoded = False
            # do not overwrite existing geometry
            if self.geometry is None:
                self.geometry = prev_obj.geometry
                self.geocoded_address = prev_obj.geocoded_address

        print type(self.geometry)
        print self.geocoded

        # geocoding against Google if we don't have a geometry
        if self.geocoded is False:
            result = Geocoder.geocode(self.address)
            if result.valid_address:
                # reverse (lat,lon) results
                coord = result[0].coordinates[::-1] 
                self.geometry = Point(coord)
                self.geocoded = True
                self.geocoded_address = str(result)
                print "geocoded %i" % (self.propertyid)

        print "updating %i" % (self.propertyid)

        super(ExpUse, self).save(*args, **kwargs)
