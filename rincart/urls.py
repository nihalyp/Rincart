from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # 👈 ഇത് ഇംപോർട്ട് ചെയ്യുക

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rincartapp.urls')),
    path('accounts/', include('allauth.urls')),
]

# ഇത് രണ്ട് വരികളും കണ്ടീഷൻ ഇല്ലാതെ ഏറ്റവും താഴെ കൊടുക്കുക:
urlpatterns += staticfiles_urlpatterns() # 👈 സ്റ്റാറ്റിക് ഫയലുകൾ വൈറ്റ്നോയിസ് വഴി റീഡ് ചെയ്യാൻ
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
