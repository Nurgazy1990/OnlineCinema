from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Hacaton Cinema API',
        default_version='v1',
        description='Кинотеатр'
    ),
    public=True
)


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('movies.urls')),
    path('api/v1/docs/', schema_view.with_ui('swagger')),
    # path('api/v1/', include('account.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)