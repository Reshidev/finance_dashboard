from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from finance.views import FinancialRecordViewSet, DashboardSummaryView
from users.views import RegisterUserView, UserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'records', FinancialRecordViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/register/', RegisterUserView.as_view()),
    path('api/users/', UserListView.as_view()),

    # Dashboard
    path('api/dashboard/', DashboardSummaryView.as_view()),

    # Router (KEEP THIS LAST)
    path('api/', include(router.urls)),
]