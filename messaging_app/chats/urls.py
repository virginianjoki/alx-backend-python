# from django.urls import path, include
# from rest_framework import routers
# from .views import ConversationViewSet, MessageViewSet
# from rest_framework_nested import routers
# from rest_framework_nested import parent_router
# from rest_framework_nested.routers import NestedDefaultRouter
# from rest_framework_nested import routers
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

# router = routers.DefaultRouter()
# convo_router = routers.NestedDefaultRouter(
#     parent_router, r'chats', lookup='chat')
# convo_router.register(r'messages', MessageViewSet,
#                       basename='conversation-messages')

# # router = routers.DefaultRouter()
# # router.register(r'conversations', ConversationViewSet, basename='conversation')
# # router.register(r'messages', MessageViewSet, basename='message')


# conversation_router = NestedDefaultRouter(
#     router, r'conversations', lookup='conversation')
# conversation_router.register(
#     r'messages', MessageViewSet, basename='conversation-messages')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]

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
]
