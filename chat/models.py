from django.db import models


class UserProfile(models.Model):

    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to='images/', null=True)
    is_bot = models.BooleanField(default=False)
    grounding_source = models.CharField(max_length=250, blank=True)
    stock_answer = models.CharField(max_length=250, blank=True)


    def __str__(self):
        return f"{self.name}"


class BotPersonality(models.Model):

    name = models.CharField(max_length=25)
    personality_type = models.CharField(max_length=250)
    portrait = models.ImageField(upload_to='images/', null=True)
    avatar = models.ImageField(upload_to='images/', null=True)
    predict_prefix = models.CharField(max_length=2048, blank=True)

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

