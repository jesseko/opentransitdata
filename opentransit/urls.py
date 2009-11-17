# NOTE: Must import *, since Django looks for things here, e.g. handler500.
from django.conf.urls.defaults import *

urlpatterns = patterns('')

# Top Level Views -- Home Page, about, etc.
urlpatterns += patterns(
    'opentransit.views.toplevel',
    url(r'^$', 'home', name='home'),
)


# Petition Views -- Currently only has examples
urlpatterns += patterns(
    'opentransit.views.petition',
    url(r'^example_petition_form$', 'example_petition_form', name='example_petition_form'),
    url(r'^example_petition_success$', 'example_petition_success', name='example_petition_success'),
)


# Feed Views -- Lists, Update Hooks, etc.
urlpatterns += patterns(
    'opentransit.views.feed',
    url(r'^update_feed_references$', 'update_feed_references', name='update_feed_references'),
    url(r'^feed_references$', 'feed_references', name='feed_references'),
)


# Agency Views -- Full URL structure for viewing agencies, and for adding/editing them
urlpatterns += patterns(
    'opentransit.views.agency',
    url('^agency/edit/(.*)$', 'edit_agency', name='edit_agency'),
    url(r'^all-agencies$', 'all_agencies'),
    url(r'^generate-slugs$', 'generate_slugs'),
    url(r'^agency/(.*)$', 'agency'),
)


# Agency Views -- Full URL structure for viewing transit apps, and for adding/editing them
urlpatterns += patterns(
    'opentransit.views.app',
    url(r'^apps/$', 'app_gallery', name='app_gallery'),
    url(r'^apps/add/$', 'add_app_form', name='add_app_form'),
    url(r'^apps/add/success/$', 'add_app_success_form', name='add_app_success_form'),
    url(r'^apps/(?P<transit_app_slug>[\w-]+)/$', 'app_details', name='app_details'),
    url(r'^apps/(?P<transit_app_slug>[\w-]+)/screenshot.png$', 'app_screenshot', name='app_screenshot'),
)