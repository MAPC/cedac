from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cedac.views.home', name='home'),
    # url(r'^cedac/', include('cedac.foo.urls')),
    (r'^$', direct_to_template, {'template': 'index.html'}),

    # TODO: add geojson view for properties
    (r'^appconfig/', 'map.views.get_app_config'),

    (r'^properties/', 'properties.views.get_properties'),

    # Grappelli
    (r'^grappelli/', include('grappelli.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()