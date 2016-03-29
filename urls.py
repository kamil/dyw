from django.conf.urls.defaults import *
from django.conf import settings
import os

from django.contrib import admin
admin.autodiscover()

from dyw.apps.rss.feeds import TasksFeed,TasksAssignedFeed,TimelineFeed

rss_feeds = {
    'tasks' : TasksFeed,
    'tasks_assigned' : TasksAssignedFeed,
    'timeline' : TimelineFeed
}


urlpatterns = patterns('',
    (r'^$', 'dyw.apps.dashboard.views.show'),
    
    # projects
    (r'^projects/new/', 'dyw.apps.project.views.new'),
    (r'^projects/', 'dyw.apps.project.views.list'),
    
    
    
    # users
    (r'^crowd/', 'dyw.apps.user.views.crowd_list'),
    (r'^user/', include('dyw.apps.user.urls')),
    
    # in-project
    
    (r'^p/(?P<project>\w+)/$', 'dyw.apps.project.views.start_redirect'),
    
    # dashboard 
    
    (r'^p/(?P<project>\w+)/dashboard/$', 'dyw.apps.dashboard.views.project'),
    
    # wiki
    (r'^p/(?P<project>\w+)/wiki/attach/(?P<page>[A-Za-z0-9/_]+)/$', 'dyw.apps.wiki.views.attach'),
    (r'^p/(?P<project>\w+)/wiki/edit/(?P<page>[A-Za-z0-9/_]+)/$', 'dyw.apps.wiki.views.edit'),
    (r'^p/(?P<project>\w+)/wiki/diff/(?P<page>[A-Za-z0-9/_]+)/(?P<revpre>\d+)/(?P<rev>\d+)/$', 'dyw.apps.wiki.views.diff'),
    (r'^p/(?P<project>\w+)/wiki/(?P<page>[A-Za-z0-9/_]+)/$', 'dyw.apps.wiki.views.show'),

    # timeline
    (r'^p/(?P<project>\w+)/timeline/$', 'dyw.apps.timeline.views.list'),

    # messages
    (r'^p/(?P<project>\w+)/messages/new/$', 'dyw.apps.message.views.new'),
    (r'^p/(?P<project>\w+)/messages/$', 'dyw.apps.message.views.list'),

    # taski
    (r'^p/(?P<project>\w+)/tasks/tags/new/$', 'dyw.apps.task.views.tag_new'),
    (r'^p/(?P<project>\w+)/tasks/closed/$', 'dyw.apps.task.views.closed'),
    (r'^p/(?P<project>\w+)/tasks/new/$', 'dyw.apps.task.views.new'),
    (r'^p/(?P<project>\w+)/tasks/(?P<task>\d+)/$', 'dyw.apps.task.views.show'),
    (r'^p/(?P<project>\w+)/tasks/(?P<task>\d+)/observe/$', 'dyw.apps.task.views.observe'),
    (r'^p/(?P<project>\w+)/tasks/$', 'dyw.apps.task.views.list'),

    # milestones
    (r'^p/(?P<project>\w+)/milestones/new/$', 'dyw.apps.milestone.views.new'),
    (r'^p/(?P<project>\w+)/milestones/(?P<id>\d+)/tasks/$', 'dyw.apps.milestone.views.tasks'),
    (r'^p/(?P<project>\w+)/milestones/$', 'dyw.apps.milestone.views.list'),

    # files
    (r'^p/(?P<project>\w+)/files/add/$', 'dyw.apps.files.views.add'),
    (r'^p/(?P<project>\w+)/files/$', 'dyw.apps.files.views.list'),
    
    # team
    (r'^p/(?P<project>\w+)/team/add/$', 'dyw.apps.user.views.team_add'),
    (r'^p/(?P<project>\w+)/team/$', 'dyw.apps.user.views.team_list'),
    (r'^p/(?P<project>\w+)/team/ac/$', 'dyw.apps.user.views.team_xhr_ac'),
    
    
    
    # projekt
    (r'^p/(?P<project>\w+)/edit/$', 'dyw.apps.project.views.edit'),
    (r'^p/(?P<project>\w+)/edit/backup/$', 'dyw.apps.project.views.backup'),
    
    
    # rss
    
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', { 'feed_dict': rss_feeds }),
    
    # tylko xhr ( tymczasowo tak )
    (r'^xhr/preview/$', 'dyw.apps.task.views.xhr_preview'),
    
    # tylko xhr ( tymczasowo tak )
    (r'^register/$', 'dyw.apps.user.views.register'),
    
    (r'^changelog/$', 'dyw.apps.system.views.changelog'),
    (r'^admin/(.*)', admin.site.root),
)
# if settings.DEBUG nie dziala :(
urlpatterns += patterns('',
        (r'^s/(?P<path>.*)$', 'django.views.static.serve', {'document_root': "%s/" % os.path.join(os.path.dirname(os.path.abspath(__file__)), "media"), 'show_indexes': True})
)

