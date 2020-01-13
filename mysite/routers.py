from rest_framework import routers
from prashnottari.viewsets import QuestionViewSet

router = routers.DefaultRouter()
router.register('questions', QuestionViewSet)
