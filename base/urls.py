from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students_base/', include('students_base.urls')),
    path('', RedirectView.as_view(url='/students_base/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
