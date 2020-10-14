from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
	path('admin/', admin.site.urls),
	path('customuser/', include('customuser.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
	path('', TemplateView.as_view(template_name='home.html'), name='home'),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
	]