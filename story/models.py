from django.db import models
from .urlgenerator import create_urlcode
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime
from story.resetkey import secure_key
from django.db.models import F


class Story(models.Model):

    class Meta:
        # Model for story posts
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
        ordering = ['created']

    author = models.ForeignKey(User, default=0, verbose_name='Author')
    title = models.CharField(max_length=160, verbose_name='Title')
    text = models.TextField(max_length=3000, verbose_name='Story')
    categories = (
    ("Funny", "Funny"),
    ("Mysterious", "Mysterious")
    )
    category = models.CharField(choices=categories, max_length=15, verbose_name='Category')
    languages = (
        ('English', 'English'),
    )
    language = models.CharField(choices=languages, max_length=10, verbose_name='Language')
    popularity = models.IntegerField(default=0, verbose_name='Popularity')
    urlcode = models.CharField(max_length=7, blank=True, unique=True, verbose_name='Link Code')
    active = models.BooleanField(default=True, verbose_name='Active')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.urlcode is None or self.urlcode == '':
            self.urlcode = create_urlcode(self)
        super(Story, self).save(*args, **kwargs)

    def __str__(self):
        return "{title} - {urlcode}".format(title=self.title, urlcode=self.urlcode)

    def get_absolute_url(self):
        return reverse('storyPage', kwargs={'shortcode': self.urlcode})


class Notification(models.Model):

    class Meta:
        # Model for users' notifications
        verbose_name = "Notification"

    owner = models.ForeignKey(User, on_delete=models.CASCADE) # will get the notification.
    notifier = models.CharField(max_length=15) # user who sends notification.
    choices = (
        ('Story', 'Story'),
        ('CommentLike', 'CommentLike'),
        ('Comment', 'Comment'),
    )
    kind = models.CharField(choices=choices, max_length=15) # which model is sending it
    conn = models.CharField(max_length=10) # story urlcode or comment id
    read = models.BooleanField(default=False) # notitification read status
    notify_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "Owner: {owner} - Notifier: {notifier}".format(owner=self.owner, notifier=self.notifier)


class Vote(models.Model):

    class Meta:
        # Model for story Votes
        verbose_name = "Vote"
        unique_together = ('user', 'story')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    choices = (
        ('Upvote', 'Upvote'),
        ('Downvote', 'Downvote'),
    )
    vote = models.CharField(choices=choices, max_length=10, verbose_name='Vote')

    def __str__(self):
        return "{story} was voted as {vote}".format(story=self.story, vote=self.vote)

    def save(self, *args, **kwargs):
        # Change popularity of related post while saving
        if not __class__.objects.filter(user=self.user, story=self.story):
            if self.vote == "Upvote":
                Story.objects.filter(pk=self.story.pk).update(popularity=F('popularity')+3)
            elif self.vote == "Downvote":
                Story.objects.filter(pk=self.story.pk).update(popularity=F('popularity')-2)
        else:
            if self.vote == "Upvote":
                Story.objects.filter(pk=self.story.pk).update(popularity=F('popularity')+5)
            elif self.vote == "Downvote":
                Story.objects.filter(pk=self.story.pk).update(popularity=F('popularity')-5)
        super(Vote, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Change popularity of related post while saving
        print("dfsdf")
        if self.vote == "Upvote":
            Story.objects.filter(pk=self.story.pk).update(popularity=F('popularity')-3)
        elif self.vote == "Downvote":
            Story.objects.filter(pk=self.story.pk).update(popularity=F('popularity')+2)
        super(Vote, self).delete(*args, **kwargs)


class StoryComment(models.Model):

    class Meta:
        # Model for comments of story
        verbose_name = 'Comment'
        ordering = ['-comment_date']

    post_itself = models.ForeignKey(Story, on_delete=models.CASCADE, verbose_name='Post')
    commentator = models.ForeignKey(User, verbose_name='Commentator')
    comment = models.TextField(max_length=250, verbose_name='Comment')
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{storycode} - {comment_id}".format(storycode=self.post_itself.title, comment_id=self.pk)

    def save(self, *args, **kwargs):
        # If user comments on the story for the first time, change popularity by 2
        if not __class__.objects.filter(commentator=self.commentator, post_itself=self.post_itself):
            Story.objects.filter(pk=self.post_itself.pk).update(popularity=F('popularity')+2)
        super(StoryComment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # If user deletes his/her last comment on the story, change popularity by -2
        if __class__.objects.filter(commentator=self.commentator, post_itself=self.post_itself).count() == 1:
            Story.objects.filter(pk=self.post_itself.pk).update(popularity=F('popularity')-2)
        super(StoryComment, self).delete(*args, **kwargs)


class CommentLike(models.Model):

    class Meta:
        # Model for comment likes
        verbose_name = 'Comment Like'
        ordering = ['user']

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(StoryComment, on_delete=models.CASCADE)

    def __str__(self):
        return "{story} - {comment} - {user}".format(story=self.comment.post_itself.urlcode, comment=self.comment.pk, user=self.user.username)

    def save(self, *args, **kwargs):
        # If any user likes any comment of the post, change popularity of the post by +1
        Story.objects.filter(pk=self.comment.post_itself.pk).update(popularity=F('popularity')+1)
        super(CommentLike, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print("dfsdfdfsdfsdf")
        # If any user dislikes any comment of the post, change popularity of the post by -1
        Story.objects.filter(pk=self.comment.post_itself.pk).update(popularity=F('popularity')-1)
        super(CommentLike, self).delete(*args, **kwargs)


class Profile(models.Model):

    class Meta:
        # Model for Users' profile details
        verbose_name = 'User Profile Detail'
        ordering = ['user']

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    genders = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=genders, blank=True, null=True, verbose_name='Gender')
    birthday = models.DateField(null=True, blank=True, verbose_name='Birthday')
    confirmed = models.BooleanField(default=False, verbose_name="Email Confirmed")
    # TODO: Add Country info for e very user

    def __str__(self):
        return "User Details for: {user}".format(user=self.user.username)


class PostReport(models.Model):

    class Meta:
        # Model for post reports
        verbose_name = 'Post Report'
        ordering = ['story']

    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    report_text = models.TextField(max_length=300, verbose_name='Report')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "{urlcode} - {story_title}".format(urlcode=self.story.urlcode, story_title=self.story.title)


class Confirmation(models.Model):

    class Meta:
        # Model for storing e-mail and password confirmatin key
        verbose_name = "Confirmation Key"
        ordering = ["user"]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length = 69, unique=True, verbose_name="Key")

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        self.key = secure_key(self)
        super(Confirmation, self).save(*args, **kwargs)


class PasswordReset(models.Model):

    class Meta:
        # Model for resetting account Password
        verbose_name = "Password Reset Key"
        ordering = ["user"]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=69, unique=True, verbose_name="Key")

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        self.key = secure_key(self)
        super(PasswordReset, self).save(*args, **kwargs)
