from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Администрирование 5.45"
admin.site.site_title = "5.45 Админ панель"
admin.site.index_title = "Добро пожаловать в панель администрирования 5.45!"
admin.site.site_url = ''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('site_api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
