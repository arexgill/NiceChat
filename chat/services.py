# chat/services.py
import logging
from .models import Messages


class AIReplyService:
    @staticmethod
    def fetch_response_from_llm(receiver):

        return "Thank you for your message! This is an automatic response."

    @staticmethod
    def create_message_and_automatic_response(sender, receiver, content):
        original_message = Messages.objects.create(sender=sender, receiver=receiver, content=content)

        automatic_response_content = AIReplyService.fetch_response_from_llm(receiver)
        automatic_response = Messages.objects.create(
            sender=receiver,
            receiver=sender,
            content=automatic_response_content,
        )

        return original_message





