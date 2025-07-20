from django.urls import path, include
# from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework_nested import routers
router = routers.DefaultRouter()
convo_router = routers.NestedDefaultRouter(
    router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet,
                      basename='conversation-messages')

# router = routers.DefaultRouter()
# router.register(r'conversations', ConversationViewSet, basename='conversation')
# router.register(r'messages', MessageViewSet, basename='message')


conversation_router = NestedDefaultRouter(
    router, r'conversations', lookup='conversation')
conversation_router.register(
    r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
]
