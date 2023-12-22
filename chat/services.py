from .models import Message, UserProfile, BotPersonality
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
    def create_message_and_automatic_response(sender, receiver, content, personality: BotPersonality):
        original_message = Message.objects.create(sender=sender, receiver=receiver, content=content)

        # Constructing the prompt with conditional statements and improved formatting
        prompt_template = (
            f"{personality.predict_prefix}\n"
            
            f"Hello {personality.name},\n\n" 
            
            "<Instruction>\n"
            f"{personality.prompt_instruction}\n\n" if personality.prompt_instruction else ""
            
            "<Context>\n"
            "Please answer this question truthfully:\n"
            f"{content}\n\n"
            
            "<Tone>\n"
            f"Use this tone when you answer: {personality.tone}\n\n" if personality.tone else ""
            
            "<Keywords>\n"
            f"{personality.keywords}\n" if personality.keywords else ""
        )

        # Removing extra newlines and leading/trailing whitespace
        prompt = '\n'.join(line.strip() for line in prompt_template.strip().split('\n'))

        automatic_response_content = AIReplyService.fetch_response_from_llm(receiver, prompt)
        automatic_response = Message.objects.create(
            sender=receiver,
            receiver=sender,
            content=automatic_response_content,
        )

        return original_message
