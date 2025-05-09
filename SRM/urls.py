from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
app_name = 'users'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("users.urls"), name="users"),
    path('', include('sr.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
