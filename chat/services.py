from .models import Message, UserProfile
from .convo import Convo


class AIReplyService:
    @staticmethod
    def fetch_response_from_llm(receiver, content: str):
        user = UserProfile.objects.get(id=receiver.id)
        if user.is_bot:
            c = Convo()
            return c.predict(content, user.grounding_source)
        else:
            return "This is an automated response. Please set up the LLM to converse"

    @staticmethod
    def create_message_and_automatic_response(sender, receiver, content, personality):
        original_message = Message.objects.create(sender=sender, receiver=receiver, content=content)

        content = content + personality

        automatic_response_content = AIReplyService.fetch_response_from_llm(receiver, content)
        automatic_response = Message.objects.create(
            sender=receiver,
            receiver=sender,
            content=automatic_response_content,
        )

        return original_message





