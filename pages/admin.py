from django.contrib import admin
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *

# Register your models here.

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("username", "is_active")
    search_fields = ("username",)


@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Conversation)
class ConversationAdmin(ModelAdmin):
    list_display = ("id", "user1", "user2", "topic", "started_at", "ended_at")
    list_filter = ("topic",)
    search_fields = ("user1__username", "user2__username")


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ("conversation", "sender", "content", "timestamp")
    search_fields = ("sender__username", "content")


@admin.register(Report)
class ReportAdmin(ModelAdmin):
    list_display = ("reporter", "reported_user", "created_at", "reviewed")
    list_filter = ("reviewed",)
    search_fields = ("reporter__username", "reported_user__username")


@admin.register(Feedback)
class FeedbackAdmin(ModelAdmin):
    list_display = ("user", "conversation", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("user__username",)


@admin.register(PostTag)
class PostTagAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")
    search_fields = ("title", "content", "author__username")
    list_filter = ("created_at",)
    filter_horizontal = ("tags",)

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    pass