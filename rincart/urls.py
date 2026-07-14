from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rincartapp.urls')),
    path('accounts/', include('allauth.urls')),
]

# ഈ വരികൾ ഒരു കണ്ടീഷനും ഇല്ലാതെ നേരിട്ട് ഏറ്റവും താഴെ ചേർക്കുക:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
