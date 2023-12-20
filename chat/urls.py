
from django.urls import path
from chat.views import (
    FriendsListView,
    SearchView,
    AddFriendView,
    ChatView,
    MessageListView,
    IndexView,
    MessageCreateView,
    ChatTemplateView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', SearchView.as_view(), name='search'),
    path('friends/<int:id>/', FriendsListView.as_view(), name='friends-list'),
    path('add-friend/<str:name>/', AddFriendView.as_view(), name='add-friend'),
    path('chat/<str:username>/', ChatView.as_view(), name='chat'),
    path('api/messages/<str:sender>/<str:receiver>/', MessageListView.as_view(), name='message-detail'),
    path('api/messages', MessageListView.as_view(), name='message-list'),
    path('api/messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('demo/', ChatTemplateView.as_view(), name='chat'),

]
