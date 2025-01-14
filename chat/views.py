from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Message, BotPersonality
from .utils import get_friends_list, get_user_id
from .serializers import MessageSerializer, UserProfileSerializer
from .services import AIReplyService
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from .models import UserProfile
from django.views.generic import TemplateView

DEFAULT_PERSONALITY_ID = 1


class ChatTemplateView(TemplateView):
    template_name = 'chat/chat_template.html'  # Path to your HTML template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AllMessagesView(APIView):
    def get(self, request, sender_id, receiver_id):
        messages = Message.objects.filter(sender=sender_id, receiver=receiver_id) | \
                   Message.objects.filter(sender=receiver_id, receiver=sender_id)
        # messages = messages.order_by('-id')  # Assuming you want the newest first
        messages_data = [
            {
                'id': message.id,
                'sender_id': message.sender_id,
                'receiver_id': message.receiver_id,
                'content': message.content,
                'time': message.time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for message in messages
        ]
        return JsonResponse(messages_data, safe=False)


class IndexView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In!")
            return render(request, "chat/index.html", {})
        else:
            username = request.user.username
            id = get_user_id(username)
            friends = get_friends_list(id)
            return render(request, "chat/Base.html", {'friends': friends})


class FriendsListView(APIView):

    def get(self, request, id):
        try:
            user = UserProfile.objects.get(id=id)
            ids = list(user.friends_set.all())
            friends = [UserProfile.objects.get(id=int(str(id))) for id in ids]
            return Response(friends)
        except UserProfile.DoesNotExist:
            return Response([])


class SearchView(TemplateView):
    template_name = "chat/search.html"

    def get(self, request, *args, **kwargs):
        users = list(UserProfile.objects.all().exclude(username=request.user.username))

        try:
            users = users[:10]
        except:
            users = users[:]

        id = get_user_id(request.user.username)
        friends = get_friends_list(id)

        return self.render_to_response({'users': users, 'friends': friends})

    def post(self, request, *args, **kwargs):
        query = request.data.get("search")
        users = [user for user in UserProfile.objects.all() if query in user.name or query in user.username]

        return self.render_to_response({'users': users})

    def post(self, request):
        query = request.data.get("search")
        users = [user for user in UserProfile.objects.all() if query in user.name or query in user.username]

        # Serialize UserProfile objects to dictionaries
        serialized_users = [UserProfileSerializer(user).data for user in users]

        return Response({'users': serialized_users})

    def get_user_id(self, username):
        use = UserProfile.objects.get(username=username)
        return use.id

    def get_friends_list(self, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
            ids = list(user.friends_set.all())
            friends = [UserProfile.objects.get(id=int(str(id))) for id in ids]
            return friends
        except UserProfile.DoesNotExist:
            return []


class AddFriendView(View):
    def get(self, request, name):
        username = request.user.username
        id = get_user_id(username)
        friend = UserProfile.objects.get(username=name)
        curr_user = UserProfile.objects.get(id=id)

        ls = curr_user.friends_set.all()
        flag = 0
        for user in ls:
            if user.friend == friend.id:
                flag = 1
                break

        if flag == 0:
            print("Friend Added!!")
            curr_user.friends_set.create(friend=friend.id)
            friend.friends_set.create(friend=id)

        # Specify the URL to redirect to after adding a friend
        redirect_url = "/search/"
        return redirect(redirect_url)


class ChatView(APIView):
    def get(self, request, username):
        friend = UserProfile.objects.get(username=username)
        curr_user_id = get_user_id(request.user.username)
        curr_user = UserProfile.objects.get(id=curr_user_id)
        messages = (Message.objects.filter(sender=curr_user_id, receiver=friend.id) |
                    Message.objects.filter(sender=friend.id, receiver=curr_user_id))
        recent_messages = messages[:20]
        friends = get_friends_list(curr_user_id)

        # If the friend is a bot, get its personalities
        personalities = friend.personalities.all() if friend.is_bot else None

        return render(request, "chat/messages.html", {
            'messages': recent_messages,
            'friends': friends,
            'curr_user': curr_user,
            'friend': friend,
            'personalities': personalities  # Include personalities in the context
        })


@method_decorator(csrf_exempt, name='dispatch')
class MessageListView(View):
    def get(self, request, sender=None, receiver=None):
        if sender is not None and receiver is not None:
            messages = Message.objects.filter(sender=sender, receiver=receiver, seen=False)
            serializer = MessageSerializer(messages, many=True, context={"request": request})
            for message in messages:
                message.seen = True
                message.save()
            return JsonResponse(serializer.data, safe=False)

    def post(self, request, sender=None, receiver=None):
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            # Extract the personality_id from the request data
            personality_id = data['personality_id'] if data['personality_id'] is not None else DEFAULT_PERSONALITY_ID

            # Optionally, fetch the BotPersonality object (if personality_id is provided)
            personality = None
            if personality_id:
                try:
                    personality = BotPersonality.objects.get(pk=personality_id)
                except BotPersonality.DoesNotExist:
                    return JsonResponse({'error': 'Personality not found'}, status=400)

            # Create the message and automatic response using the provided personality
            AIReplyService.create_message_and_automatic_response(
                sender=serializer.validated_data['sender'],
                receiver=serializer.validated_data['receiver'],
                content=serializer.validated_data['content'],
                personality=personality  # Pass the BotPersonality object to the service
            )
            return JsonResponse({}, status=201)

        return JsonResponse(serializer.errors, status=400)


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Use the service to create the original message and automatic response
        original_message = AIReplyService.create_message_and_automatic_response(
            sender=serializer.validated_data['sender'],
            receiver=serializer.validated_data['receiver'],
            content=serializer.validated_data['content'],
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
