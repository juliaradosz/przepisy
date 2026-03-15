from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse

def service_worker(request):
    sw_path = settings.BASE_DIR / 'static' / 'sw.js'
    return FileResponse(open(sw_path, 'rb'), content_type='application/javascript',
                        headers={'Service-Worker-Allowed': '/'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sw.js', service_worker, name='service_worker'),
    path('', include('recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'recipes.views.handler404'
handler500 = 'recipes.views.handler500'
