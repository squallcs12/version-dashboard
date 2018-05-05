from rest_framework.routers import SimpleRouter

from dashboard.views import ServiceDeployViewSet

route = SimpleRouter()
route.register('servicedeploys', ServiceDeployViewSet)

urlpatterns = route.get_urls()
