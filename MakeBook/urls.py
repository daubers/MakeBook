from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'MakeBook.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', "Project.views.index"),
                       url(r'^Projects/$', "Project.views.all_projects"),
                       url(r'^Projects/Detail/(?P<newid>\d)/$', "Project.views.project_detail"),
                       url(r'^Projects/New/$', "Project.views.new_project"),
                       url(r'^Projects/New/Create/$', "Project.views.create_new_project"),
                       url(r'^admin/', include(admin.site.urls)),
)
