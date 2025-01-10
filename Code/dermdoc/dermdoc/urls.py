from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("account.urls")),
    path('child/', include("child.urls")),
]
