# Imports
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views

# URL patterns
urlpatterns = [path(settings.ADMIN_URL, admin.site.urls)]

# App URL patterns
urlpatterns += [
    path("", include("apps.core.urls", namespace="core")),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
]

# If the project is in debug mode
if settings.DEBUG:
    # Add error pages
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

# Admin configuration
admin.site.site_header = "LeadTrack"
admin.site.site_title = "LeadTrack Admin Portal"
admin.site.index_title = "Welcome to LeadTrack Admin Portal"
