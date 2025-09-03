from django.contrib import admin
from django.urls import path, include
from inventory_app import views as inventory_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/signup/", inventory_views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("inventory_app.urls")),
]

# This is for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
