from django.contrib import admin
from .models import (Story,
                    StoryUpvotes,
                    StoryDownvotes,
                    StoryComment,
                    Profile,
                    CommentLike,
                    PostReport,
                    Notification)

# Register your models here.

admin.site.register(Story)
admin.site.register(StoryUpvotes)
admin.site.register(StoryDownvotes)
admin.site.register(StoryComment)
admin.site.register(Profile)
admin.site.register(CommentLike)
admin.site.register(PostReport)
admin.site.register(Notification)
