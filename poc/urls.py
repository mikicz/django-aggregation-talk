"""
URL configuration for poc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static


from django.conf import settings
from visits.views.aggregate import AggregateView, AggregateViewWithUser
from visits.views.materialized_view import MaterializedViewView
from visits.views.view import ViewView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("aggregate/", AggregateView.as_view()),
    path("aggregate-with-user/", AggregateViewWithUser.as_view()),
    path("view/", ViewView.as_view()),
    path("materialized-view/", MaterializedViewView.as_view()),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
