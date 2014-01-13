from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'MakeBook.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', "Project.views.index"),
                       url(r'^Projects/$', "Project.views.all_projects"),
                       url(r'^Projects/Detail/(?P<newid>\d+)/$', "Project.views.project_detail"),
                       url(r'^Projects/New/$', "Project.views.new_project"),
                       url(r'^Projects/New/Create/$', "Project.views.create_new_project"),

                       url(r'^BoM/New/$', "Project.views.create_bom"),
                       url(r'^BoM/New/Create/$', "Project.views.create_bom_ajax"),
                       url(r'^BoM/Detail/(?P<bomid>\d+)/$', "Project.views.bom_detail"),

                       url(r'^Parts/New/Create/$', "Project.views.new_part"),

                       url(r'^admin/', include(admin.site.urls)),
)
