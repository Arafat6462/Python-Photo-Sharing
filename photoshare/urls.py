from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('photos.urls')),
]

# Serve media files in development and production.
# In a high-traffic production environment, it's recommended to use a dedicated web server 
# like Nginx or a cloud storage service, but this is a simple and effective solution for this setup.
if settings.DEBUG or not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
