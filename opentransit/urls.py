# NOTE: Must import *, since Django looks for things here, e.g. handler500.
from django.conf.urls.defaults import *

urlpatterns = patterns('')

urlpatterns += patterns(
    'opentransit.views',
    url(r'^$', 'home', name='home'),
    url(r'^example_petition_form$', 'example_petition_form', name='example_petition_form'),
    url(r'^example_petition_success$', 'example_petition_success', name='example_petition_success'),
    url(r'^update_feed_references$', 'update_feed_references', name='update_feed_references'),
    url(r'^feed_references$', 'feed_references', name='feed_references'),
    url('^agency/edit/(.*)$', 'edit_agency', name='edit_agency'),
    url(r'^all-agencies$', 'all_agencies'),
    
    url(r'^apps/$', 'app_gallery', name='app_gallery'),
    url(r'^apps/add/$', 'add_app_form', name='add_app_form'),
    url(r'^apps/add/success/$', 'add_app_success_form', name='add_app_success_form'),
    url(r'^apps/(?P<transit_app_slug>[\w-]+)/$', 'app_details', name='app_details'),
    url(r'^apps/(?P<transit_app_slug>[\w-]+)/screenshot.png$', 'app_screenshot', name='app_screenshot'),
)
