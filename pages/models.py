from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.db import models
from django.utils import timezone



# Optional: tag for mental health topics
class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Represents a peer-to-peer conversation session
class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_started')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_joined')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Chat between {self.user1} & {self.user2}"

# Messages within a conversation
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"

# Report system for abuse or inappropriate behavior
class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reporter} reported {self.reported_user}"

# Optional: feedback from users after chats
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, "😔"), (2, "😐"), (3, "🙂"), (4, "😊"), (5, "❤️")])
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user} - {self.rating}"


# Tags for posts
class PostTag(models.Model):
    ICON_CHOICES = [
        ('fas fa-bell', 'Bell'),
        ('fas fa-envelope', 'Envelope'),
        ('fas fa-check-circle', 'Check Circle'),
        ('fas fa-exclamation-triangle', 'Exclamation Triangle'),
        ('fas fa-info-circle', 'Info Circle'),
        ('fas fa-times-circle', 'Times Circle'),
        ('fas fa-user', 'User'),
        ('fas fa-users', 'Users'),
        ('fas fa-cog', 'Cog'),
        ('fas fa-gear', 'Gear'),
        ('fas fa-heart', 'Heart'),
        ('fas fa-star', 'Star'),
        ('fas fa-thumbs-up', 'Thumbs Up'),
        ('fas fa-thumbs-down', 'Thumbs Down'),
        ('fas fa-comment', 'Comment'),
        ('fas fa-comments', 'Comments'),
        ('fas fa-upload', 'Upload'),
        ('fas fa-download', 'Download'),
        ('fas fa-cloud-upload-alt', 'Cloud Upload'),
        ('fas fa-cloud-download-alt', 'Cloud Download'),
        ('fas fa-truck', 'Truck'),
        ('fas fa-shipping-fast', 'Shipping Fast'),
        ('fas fa-box', 'Box'),
        ('fas fa-clipboard-check', 'Clipboard Check'),
        ('fas fa-calendar', 'Calendar'),
        ('fas fa-clock', 'Clock'),
        ('fas fa-bug', 'Bug'),
        ('fas fa-lock', 'Lock'),
        ('fas fa-unlock', 'Unlock'),
        ('fas fa-warning', 'Warning'),
        ('fas fa-question-circle', 'Question Circle'),
        ('fas fa-smile', 'Smile'),
        ('fas fa-frown', 'Frown'),
        ('fas fa-shopping-cart', 'Shopping Cart'),
        ('fas fa-credit-card', 'Credit Card'),
        ('fas fa-check', 'Check'),
        ('fas fa-times', 'Times'),
        ('fas fa-angle-double-right', 'Double Right Arrow'),
        ('fas fa-angle-double-left', 'Double Left Arrow'),
        ('fas fa-sync', 'Sync'),
        ('fas fa-spinner', 'Spinner'),
        ('fas fa-chart-line', 'Chart Line'),
        ('fas fa-bolt', 'Bolt'),
        ('fas fa-gift', 'Gift'),
        ('fas fa-tag', 'Tag'),
        ('fas fa-tags', 'Tags'),
        ('fas fa-eye', 'Eye'),
        ('fas fa-eye-slash', 'Eye Slash'),
    ]

    icon = models.CharField(max_length=100, choices=ICON_CHOICES, default='Tag')
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"#{self.name}"

# Posts shared by users (anonymous or pseudonymous)
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    tags = models.ManyToManyField(PostTag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else f"Post by {self.author}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  f"{self.user}: {self.id}"

class Hug(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='hugs')

    def __str__(self):
        return f"{self.user.username} to {self.post.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    personal_story = models.TextField(blank=True)
    interests = models.ManyToManyField(PostTag, blank=True)
    post_count = models.PositiveIntegerField(default=0)
    hugs_count = models.PositiveIntegerField(default=0)
    connections_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}"