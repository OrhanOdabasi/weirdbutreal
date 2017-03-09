from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from story.models import StoryUpvotes, CommentLike, Notification

@receiver(post_save, sender=StoryUpvotes)
def upvote_notifier(sender, created, instance, **kwargs):
    #upvote notification method
    if created:
        owner = instance.story.author
        notifier = instance.user.username
        kind = "Story"
        conn = instance.story.urlcode
        q = Notification(owner=owner, notifier=notifier, kind=kind, conn=conn)
        q.save()


@receiver(post_delete, sender=StoryUpvotes)
def dlt_story_notification(sender, instance, **kwargs):
    # this method deletes notification if upvote instance is deleted (downvoted)
    conn = instance.story.urlcode
    notifier = instance.user.username
    q = Notification.objects.filter(conn=conn, notifier=notifier)
    if q:
        q.delete()


@receiver(post_save, sender=CommentLike)
def like_notifier(sender, created, instance, **kwargs):
    # comment like notification method
    if created:
        owner = instance.comment.commentator
        notifier = instance.user.username
        kind = "Comment"
        conn = instance.comment.pk
        q = Notification(owner=owner, notifier=notifier, kind=kind, conn=conn)
        q.save()


@receiver(post_delete, sender=CommentLike)
def dlt_comment_notification(sender, instance, **kwargs):
    # this method deletes notification if comment like instance is deleted (downvoted)
    conn = instance.comment.pk
    notifier = instance.user.username
    q = Notification.objects.filter(conn=conn, notifier=notifier)
    if q:
        q.delete()
