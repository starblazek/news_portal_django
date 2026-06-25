from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('news_app.api_urls')),
    path('api/token/', obtain_auth_token, name='api_token'),
    path('', include('news_app.urls')),
]

handler404 = 'news_app.views.handler404'
handler500 = 'news_app.views.handler500'
