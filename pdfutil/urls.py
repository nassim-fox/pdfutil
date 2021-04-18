
from django.contrib import admin
from django.urls import path, include
from pdfutilApp import views
from rest_framework import routers 
from django.conf.urls import url


router = routers.DefaultRouter()
router.register(r'log',views.LogViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)), 
    path('api-auth/',include('rest_framework.urls',namespace="rest_framework")),
    url(r'^upload/(?P<filename>[^/]+)$', views.FileUploadView.as_view()),   
    url(r'^imTopdf/(?P<filename>[^/]+)$', views.ImageToPdfView.as_view()),   
    url(r'^pdfToim/(?P<filename>[^/]+)$', views.PdfToImageView.as_view())
   # path('upload/<filename>', views.FileUploadView,"file")
]
