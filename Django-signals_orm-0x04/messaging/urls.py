from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Step 1: Main router (parent)
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Step 2: Nested router for messages inside conversations
conversation_router = NestedDefaultRouter(
    router, r'conversations', lookup='conversation')
conversation_router.register(
    r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
]
