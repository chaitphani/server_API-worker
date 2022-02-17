from django.contrib import admin
from django.urls import path, include
from server_app.views import InboundApiView, OutboundApiView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls')),

    path('api/inbound/sms', InboundApiView.as_view(), name='api_inbound'),
    path('api/outbound/sms', OutboundApiView.as_view(), name='api_outbound'),

]
