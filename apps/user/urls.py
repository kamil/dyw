from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(\d+)/$', 'dyw.apps.user.views.show'),
    (r'^profile/$', 'dyw.apps.user.views.profile'),
    (r'^login/$', 'dyw.apps.user.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
)
