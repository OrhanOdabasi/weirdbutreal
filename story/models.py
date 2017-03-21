from django.db import models
from .urlgenerator import create_urlcode
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime


class Story(models.Model):

    class Meta:
        # It's the model for story posts
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
        ('En', 'English'),
        ('Tr', 'Turkish')
    )
    language = models.CharField(choices=languages, max_length=10, verbose_name='Language')
    upvotes = models.IntegerField(default=0, verbose_name='Upvotes')
    downvotes = models.IntegerField(default=0, verbose_name='Downvotes')
    popularity = models.IntegerField(blank=True, verbose_name='Popularity')
    urlcode = models.CharField(max_length=7, blank=True, unique=True, verbose_name='Link Code')
    active = models.BooleanField(default=True, verbose_name='Active')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    reports = models.IntegerField(default=0, verbose_name='Reports')


    def save(self, *args, **kwargs):
        if self.urlcode is None or self.urlcode == '':
            self.urlcode = create_urlcode(self)
            self.popularity = int(self.upvotes) - int(self.downvotes)
        super(Story, self).save(*args, **kwargs)


    def __str__(self):
        return "{author} posted '{title}'".format(author=self.author, title=self.title)


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
    kind = models.CharField(choices=choices, max_length=8) # which model is sending it
    conn = models.CharField(max_length=10) # story urlcode or comment id
    read = models.BooleanField(default=False) # notitification read status
    notify_time = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return "Owner: {owner} - Notifier: {notifier}".format(owner=self.owner, notifier=self.notifier)



class StoryUpvotes(models.Model):

    class Meta:
        # It's the model that shows who upvoted the post.
        verbose_name = 'Story Upvote'
        ordering = ['user']

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)


    def __str__(self):
        return "{user} upvoted {post}".format(user=self.user.username, post=self.story.title)



class StoryDownvotes(models.Model):

    class Meta:
        #It's the model that shows who downvoted the post.
        verbose_name = 'Story Downvote'
        ordering = ['user']

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)


    def __str__(self):
        return "{user} downvoted {post}".format(user=self.user.username, post=self.story.title)



class StoryComment(models.Model):

    class Meta:
        # It's the model of comments for stories.
        verbose_name = 'Comment'
        ordering = ['-comment_date']

    post_itself = models.ForeignKey(Story, on_delete=models.CASCADE, verbose_name='Post')
    commentator = models.ForeignKey(User, verbose_name='Commentator')
    comment = models.TextField(max_length=250, verbose_name='Comment')
    likes = models.IntegerField(default=0, verbose_name='Likes')
    comment_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{commentator} commented on {comment_id} - '{storycode}'".format(commentator=self.commentator,
                                                                                storycode=self.post_itself.title,
                                                                                comment_id=self.pk)



class CommentLike(models.Model):

    class Meta:
        # It's the Comment model for a post.
        verbose_name = 'Comment Like'
        ordering = ['user']

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(StoryComment, on_delete=models.CASCADE)


    def __str__(self):
        return "{liker} liked {comment} of {commentator}".format(liker=self.user.username,
                                                                comment=self.comment.pk,
                                                                commentator=self.comment.commentator)



class Profile(models.Model):

    class Meta:
        # It's the additional model to User Model
        verbose_name = 'User Profile Detail'
        ordering = ['user']

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    genders = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=genders, blank=True, verbose_name='Gender')
    birthday = models.DateField(null=True, blank=True, verbose_name='Birthday')


    def __str__(self):
        return "User Details for: {}".format(self.user.username)



class PostReport(models.Model):

    class Meta:
        # It's the report model for violations
        verbose_name = 'Post Report'
        ordering = ['story']

    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    report_text = models.TextField(max_length=300, verbose_name='Report')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return self.story.title
