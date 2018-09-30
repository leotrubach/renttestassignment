from rest_framework import routers
from .views import CompanyListViewSet


router = routers.SimpleRouter()
router.register(r'companies', CompanyListViewSet, base_name='company')


urlpatterns = router.urls

