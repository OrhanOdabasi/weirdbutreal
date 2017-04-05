from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from story.models import Vote, CommentLike, Notification, StoryComment, User, Profile, Confirmation, PasswordReset
from story import mails

@receiver(post_save, sender=Vote)
def upvote_notifier(sender, created, instance, **kwargs):
    #upvote notification method
    if created and instance.vote == "Upvote":
        owner = instance.story.author
        notifier = instance.user.username
        kind = "Story"
        conn = instance.story.urlcode
        q = Notification(owner=owner, notifier=notifier, kind=kind, conn=conn)
        q.save()


@receiver(post_delete, sender=Vote)
def dlt_story_notification(sender, instance, **kwargs):
    # this method deletes notification if upvote instance is deleted (downvoted)
    if instance.vote == "Upvote":
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
        kind = "CommentLike"
        conn = instance.comment.pk
        q = Notification(owner=owner, notifier=notifier, kind=kind, conn=conn)
        q.save()


@receiver(post_delete, sender=CommentLike)
def dlt_commentlike_notification(sender, instance, **kwargs):
    # this method deletes notification if comment like instance is deleted (downvoted)
    conn = instance.comment.pk
    notifier = instance.user.username
    q = Notification.objects.filter(conn=conn, notifier=notifier)
    if q:
        q.delete()


@receiver(post_save, sender=StoryComment)
def comment_notification(sender, created, instance, **kwargs):
    # comment notifier
    if created:
        owner = instance.post_itself.author
        notifier = instance.commentator.username
        kind = "Comment"
        conn = instance.pk
        q = Notification(owner=owner, notifier=notifier, kind=kind, conn=conn)
        q.save()


@receiver(post_delete, sender=StoryComment)
def dlt_comment_notification(sender, instance, **kwargs):
    # this method deletes the notification if comment instance is removed form db.
    conn = instance.pk
    notifier = instance.commentator.username
    kind = "CommentLike"
    q = Notification.objects.filter(conn=conn, notifier=notifier, kind=kind)
    if q:
        q.delete()


@receiver(post_save, sender=User)
def profile_details(sender, created, instance, **kwargs):
    # it will create an profile object when a new user is created
    if created:
        user = instance
        q = Profile.objects.filter(user=user)
        if not q:
            Profile.objects.create(user=user)


@receiver(post_save, sender=Profile)
def create_confirmation(sender, created, instance, **kwargs):
    # it triggers confirmation model to create a key for the user
    user = instance.user
    sending_mail = False
    if created:
        q = Confirmation(user=user)
        q.save()
        sending_mail = True
    else:
        if not instance.confirmed:
            q = Confirmation(user=user)
            q.save()
            sending_mail = True
        else:
            qs = Confirmation.objects.filter(user=user)
            if qs:
                qs.delete()
    # With the user's 'created' signal, sends an email to each user
    if sending_mail:
        try:
            owner = str(q.user.username)
            to_email = q.user.email
            key = q.key
            infos = """
            Username: {username}
            link: http://www.weirdbutreal.com/confirmation/{username}/{key}
            """.format(username=owner, key=key)
            response = mails.sendconfirmation(owner=owner, to_email=to_email, infos=infos)
            print(response.status_code)
        except Exception as e:
            print(e)


@receiver(post_save, sender=PasswordReset)
def passwordreset_sender(sender, created, instance, **kwargs):
    # Email sender for forgotten password
    user = instance.user
    if created:
        try:
            owner = str(user.username)
            to_email = user.email
            key = instance.key
            infos = """
            Username: {username}
            link: http://www.weirdbutreal.com/resetpassword/{username}/{key}
            """.format(username=owner, key=key)
            response = mails.sendpasswordreset(owner=owner, to_email=to_email, infos=infos)
            print(response.status_code)
        except Exception as e:
            print(e)
