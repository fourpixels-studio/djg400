"""
URL configuration for djg400 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("frontend.urls")),
    path("", include("mixes.urls")),
    path("account/", include("account.urls")),
    path("shop/", include("shop.urls")),
    path("newsletter/", include("newsletter.urls")),
    path("playlists/", include("playlists.urls")),
    path("hitcount/", include("hitcount.urls")),
    path("summernote/", include('django_summernote.urls')),
    path("remixes/", include("remixes.urls")),
    path("blogs/", include("blogs.urls")),
    path("orders/", include('orders.urls')),
    path("shop/", include("products.urls")),
    path("cart/", include("cart.urls")),
    path("", include("payments.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configure admin titles
admin.site.site_header = "DJ G400 Admin"

# Tab/Site Title
admin.site.site_header = "DJ G400"

admin.site.index_title = "DJ G400 - Admin"
