from django.contrib import admin
from .models import (Story,
                    StoryComment,
                    Profile,
                    CommentLike,
                    PostReport,
                    Notification,
                    Vote)

# Register your models here.

admin.site.register(Story)
admin.site.register(StoryComment)
admin.site.register(Profile)
admin.site.register(CommentLike)
admin.site.register(PostReport)
admin.site.register(Notification)
admin.site.register(Vote)
