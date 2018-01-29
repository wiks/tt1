from django.conf.urls import include, url
from django.contrib import admin

handler400 = 'tagspick.views.page_problem'
handler403 = 'tagspick.views.page_problem'
handler404 = 'tagspick.views.page_problem'
handler500 = 'tagspick.views.page_problem'

urlpatterns = [
    # Examples:
    # url(r'^$', 'tt1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'tagspick.views.index', name='main'),
    url(r'^0', 'tagspick.views.index0', name='index0'),
    url(r'^a', 'tagspick.views.indexa', name='indexa'),
    url(r'^testurl', 'tagspick.views.testurl', name='testurl'),
]
