from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import handler404
from .errors import handler404 as custom_404_handler


from .view import home_view

urlpatterns = [
    path('ogani/', admin.site.urls),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('', home_view, name='home'),

    # local path
    ### for example
    # path('', include('app.urls')),
    path('', include('user.urls')),
    path('', include('contact_us.urls')),
    path('', include('category.urls')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_404_handler
