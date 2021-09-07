# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'^api/post/', include("posts.api.urls")),
    url(r'^api/account/', include("account.api.urls")),
]
