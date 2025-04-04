from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static  # Импорт для работы с медиафайлами

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
    path('accounts/', include('accounts.urls')),
    path('', RedirectView.as_view(url='store/', permanent=False)),  # перенаправление с корня на store/
]

# Добавляем обработку медиафайлов только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)