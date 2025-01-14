from django.db import models


class UserProfile(models.Model):

    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to='images/', null=True)
    is_bot = models.BooleanField(default=False)
    grounding_source = models.CharField(max_length=250, blank=True)
    stock_answer = models.CharField(max_length=250, blank=True)
    personalities = models.ManyToManyField('BotPersonality', related_name='users', blank=True)

    def __str__(self):
        return f"{self.name}"


class BotPersonality(models.Model):

    name = models.CharField(max_length=25)
    personality_type = models.CharField(max_length=250, blank=True)
    portrait = models.ImageField(upload_to='images/', null=True, blank=True)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True)
    predict_prefix = models.CharField(max_length=2048, blank=True)

    # Bot personality profile
    prompt_instruction = models.TextField(blank=True, help_text="Instructions for crafting prompts for this personality.")
    prompt_examples = models.TextField(blank=True, help_text="Examples of effective prompts for this personality.")
    prompt_output_details = models.TextField(blank=True, help_text="Details on what the output should look like for this personality.")
    context_length = models.IntegerField(default=2048,
                                         help_text="The number of characters of conversation history to consider for each prompt.")
    tone = models.CharField(max_length=250, blank=True, help_text="The desired tone for this personality's responses.")
    keywords = models.TextField(blank=True, help_text="Key topics or words associated with this personality.")

    class Meta:
        verbose_name_plural = "bot personalities"

    def __str__(self):
        return f"{self.name}"


class Message(models.Model):

    content = models.TextField()
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver')
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.receiver} From: {self.sender}"

    class Meta:
        ordering = ('timestamp',)


class Friends(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    friend = models.IntegerField()

    class Meta:
        verbose_name_plural = "friends"


    def __str__(self):
        return f"{self.friend}"

