from django.urls import include, path
from django.contrib import admin
import notifications

from gosacco import views

authpatterns = [
    path('token-auth/', views.obtain_jwt_token),
    path('token-refresh/', views.refresh_jwt_token),
    path('registration/', views.AccountView.as_view()),
]

apipatterns = [
    path('members/', include('members.member_urls')),
    path('groups/', include('members.group_urls')),
    path('auth/', include(authpatterns)),
    # path('shares/', include('shares.urls')),
    # path('savings/', include('savings.urls')),
    # path('loans/', include('loans.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include('rest_framework_swagger.urls')),
    path('api/', include(apipatterns)),
    path('inbox/notifications/', include(notifications.urls)),
]

admin.site.site_header = 'GoSacco'
admin.site.site_title = 'GoSacco'
admin.site.index_title = 'Administration'

