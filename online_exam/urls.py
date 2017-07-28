"""online_exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler404
from django.contrib import admin
from material.frontend import urls as frontend_urls
# from Exam_portal.ajax import *
from Exam_portal.views import register, admin_auth, python_class

urlpatterns = [
    url(r'^admin/', admin_auth, name="admin_auth"),

    url(r'^exam/', include('Exam_portal.urls', namespace="Exam_portal")),
    url(r'', include(frontend_urls)),
    # url(r'^$', python_class, name="python"),
    url(r'^$', register, name="register"),
    url(r'^godadmin/', admin.site.urls),

   ]
handler404 = "Exam_portal.views.custom404"
