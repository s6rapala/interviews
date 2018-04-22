"""interviews_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from rest_framework_nested import routers

from interviews import views

router = routers.DefaultRouter()
router.register(r'employees', views.EmployeeViewSet)
router.register(r'timeslots', views.AvailableTimeSlotsList, base_name='timeslots')

domains_router = routers.NestedSimpleRouter(router, r'employees', lookup='employee')
domains_router.register(r'timeslots', views.EmployeeAvailabilityViewSet, base_name='employee-timeslots')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(domains_router.urls)),
    # url(r'^api/employees/$', views.EmployeeList),
    # url(r'^api/employees/(?P<pk>\d+)/$', views.EmployeeAvailabilityViewSet, name='retrieve'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
