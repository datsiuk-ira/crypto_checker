from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('market_analysis/', include('market_analysis.urls')),
]
