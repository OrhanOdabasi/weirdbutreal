from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.contrib import messages
from django.views import View

from .models import (Story,
                    StoryComment,
                    StoryUpvotes,
                    StoryDownvotes,
                    CommentLike,
                    Profile,
                    Notification)
from .forms import (PostStoryForm,
                    LoginForm,
                    SignupForm,
                    SearchPostForm,
                    ProfileEditForm,
                    UserEditForm,
                    LeaveComment,
                    ReportStory)

# post per page
ppp = 10

# entry per top menu
eptm = 5
def latestStories(eptm):
    # Create your views here.
    latest_f = Story.objects.filter(category="Funny").order_by("-popularity")[:eptm]
    latest_m = Story.objects.filter(category="Mysterious").order_by("-popularity")[:eptm]
    latest_a = Story.objects.all().order_by("-popularity")[:eptm]
    return latest_f, latest_m, latest_a


def getNotifications(user, last):
    notifications = Notification.objects.filter(owner=user)
    unread = notifications.filter(read=False).count()
    notifications = notifications.order_by('-notify_time')[:last]
    return unread, notifications

# Views methods

def homepage(request):
    # Home Page
    stories = Story.objects.all().order_by("-created")
    paginator = Paginator(stories, ppp)
    page = request.GET.get('page')

    try:
        story_list = paginator.page(page)
    except PageNotAnInteger:
        story_list = paginator.page(1)
    except EmptyPage:
        story_list = paginator.page(paginator.num_pages)

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'stories' : story_list,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'listing/index.html', context)


def funny(request):
    # Funny section of the site
    stories = Story.objects.filter(category='Funny').order_by("-modified")
    paginator = Paginator(stories, ppp)
    page = request.GET.get('page')

    try:
        story_list = paginator.page(page)
    except PageNotAnInteger:
        story_list = paginator.page(1)
    except EmptyPage:
        story_list = paginator.page(paginator.num_pages)

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'stories' : story_list,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'listing/funny.html', context)


def mysterious(request):
    # Mystery section of the site
    stories = Story.objects.filter(category='Mysterious').order_by("-modified")
    paginator = Paginator(stories, ppp)
    page = request.GET.get('page')

    try:
        story_list = paginator.page(page)
    except PageNotAnInteger:
        story_list = paginator.page(1)
    except EmptyPage:
        story_list = paginator.page(paginator.num_pages)

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'stories' : story_list,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'listing/mysterious.html', context)


@login_required(redirect_field_name='redirect', login_url='/login')
def notifications(request):
    # simple notification system
    allnotifications = Notification.objects.filter(owner=request.user)
    for each in allnotifications:
        each.read = True
        each.save()

    notification_list = allnotifications.order_by('-notify_time')[:20]

    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)

    latest_f, latest_m, latest_a = latestStories(eptm)
    context = {
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'notification_list' : notification_list,
        'unread' : unread,
    }
    return render(request, 'profile/notifications.html', context)

"""
# TODO: Undone profile system
@login_required(redirect_field_name='redirect', login_url='/login')
def profile(request):
    # Users' profile details
    context = {
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
    }
    return render(request, 'profile/myprofile.html', context)
"""

def help(request):
    # Help and FAQ page of the site
    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'misc/help.html', context)


def about(request):
    # Simple page about site and the programmer
    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'misc/about.html', context)


def story(request, shortcode):
    # Story Page
    qs = get_object_or_404(Story, urlcode=shortcode)
    comment_count = qs.storycomment_set.count()
    if qs.storycomment_set:
        # list comments
        comments = qs.storycomment_set.all().annotate(topvotes=Count('commentlike'))
        comments= comments.order_by('-topvotes', '-comment_date')
    else:
        comments = False

    commentform = LeaveComment()

    if request.method == 'POST':
        form = LeaveComment(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post_itself = qs
            obj.commentator = request.user
            obj.save()
            return redirect(qs)

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    if qs and qs.active:
        context = {
        'post' : qs,
        'comment_count': comment_count,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'comments' : comments,
        'commentform': commentform,
        'notifications' : notifications,
        'unread' : unread,
        }
    return render(request, 'listing/story.html', context)


@login_required(redirect_field_name='redirect', login_url='/login')
def submitstory(request):
    # Form submit page
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostStoryForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.author = request.user
                obj.save()
                new_obj = Story.objects.get(id=obj.id)
                return redirect(new_obj)

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'form': PostStoryForm,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'forms/post-story.html', context)


def login_view(request):
    # Login page
    if request.user.is_authenticated:
        return redirect(reverse('profilePage'))

    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(reverse('homePage'))

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'form' : form,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'registration/login.html', context)


def logout_view(request):
    # Logout page
    logout(request)
    return redirect(reverse('homePage'))


def register(request):
    # registration page
    if request.user.is_authenticated:
        return redirect(reverse('profilePage'))

    form = SignupForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        new_user.set_password(password)
        new_user.save()

        user = authenticate(username=new_user.username, password=password)
        login(request, user)
        return redirect(reverse('editprofilePage'))

    latest_f, latest_m, latest_a = latestStories(eptm)
    context = {
        'form' : form,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
    }
    return render(request, 'registration/signup.html', context)


# TODO: Undone passreminder page
def passReminder(request):
    # password remider page
    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'registration/pass_reminder.html', context)


@login_required(redirect_field_name='redirect', login_url='/login')
def myposts(request):
    # users' post list
    if request.user.is_authenticated:
        qs = get_object_or_404(User, username=request.user)
        story_list = qs.story_set.all().order_by('-modified')
    else:
        return redirect(reverse('loginPage'))

    paginator = Paginator(story_list, 20)
    page = request.GET.get('page')
    try:
        story_ls = paginator.page(page)
    except PageNotAnInteger:
        story_ls = paginator.page(1)
    except EmptyPage:
        story_ls = paginator.page(paginator.num_pages)

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'stories' : story_ls,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'profile/myposts.html', context)


@login_required(redirect_field_name='redirect', login_url='/login')
def mycomments(request):
    # users' comment list
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        my_comments = StoryComment.objects.filter(commentator=user)
    else:
        return redirect(reverse('loginPage'))

    paginator = Paginator(my_comments, 20)
    page = request.GET.get('page')
    try:
        comment_list = paginator.page(page)
    except PageNotAnInteger:
        comment_list = paginator.page(1)
    except EmptyPage:
        comment_list = paginator.page(paginator.num_pages)

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'stories' : comment_list,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'profile/mycomments.html', context)


def myupvotes(request):
    # users' post upvotes list
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        my_upvotes = StoryUpvotes.objects.filter(user=user)
    else:
        return redirect(reverse('loginPage'))

    paginator = Paginator(my_upvotes, 20)
    page = request.GET.get('page')
    try:
        upvote_list = paginator.page(page)
    except PageNotAnInteger:
        upvote_list = paginator.page(1)
    except EmptyPage:
        upvote_list = paginator.page(paginator.num_pages)

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'my_upvotes' : upvote_list,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'profile/myupvotes.html', context)


def mydownvotes(request):
    # users' post upvotes list
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        my_downvotes = StoryDownvotes.objects.filter(user=user)
    else:
        return redirect(reverse('loginPage'))

    paginator = Paginator(my_downvotes, 20)
    page = request.GET.get('page')
    try:
        downvote_list = paginator.page(page)
    except PageNotAnInteger:
        downvote_list = paginator.page(1)
    except EmptyPage:
        downvote_list = paginator.page(paginator.num_pages)

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'my_downvotes' : downvote_list,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'profile/mydownvotes.html', context)


def searchpost(request):
    # searchs posts only
    query = request.GET.get("searchq")
    if query and len(query)>3 and len(query)<25:
        form = SearchPostForm(initial={'searchq': query})
        story_list = Story.objects.filter(
            Q(title__icontains=query)|
            Q(text__icontains=query)
        ).order_by("-created").distinct()

        paginator = Paginator(story_list, ppp)
        page = request.GET.get('page')
        try:
            story_list = paginator.page(page)
        except PageNotAnInteger:
            story_list = paginator.page(1)
        except EmptyPage:
            story_list = paginator.page(paginator.num_pages)
        if not story_list:
            messages.warning(request, "No way! We don't have a weird story about it!")
        context = {
            'query' : query,
            'stories' : story_list,
        }
    else:
        form = SearchPostForm()
        context = {}
        messages.warning(request, "Search term must contain at least 4 max 24 characters")

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context.update( {
        'form' : form,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    })
    return render(request, 'listing/search.html', context)


# TODO: something wrong
@login_required(redirect_field_name='redirect', login_url='/login')
def editprofile(request):
    # edit your user profile
    qs = get_object_or_404(User, username=request.user)
    #qs2 = get_object_or_404(Profile, user=request.user)
    # burayı hallet
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = UserEditForm(request.POST, instance=qs, prefix="formone")
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Profile has been updated successfully!')
            else:
                messages.warning(request, form.errors.as_text())
    form = UserEditForm(instance=qs, prefix="formone")

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'form' : form,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'forms/edit-profile.html', context)


def profilepostlist(request, profile):
    # post list of an author, it will list when post author link is clicked
    if request.user.is_authenticated:
        qs = get_object_or_404(User, username=profile)
        story_list = qs.story_set.all().order_by('-modified')
    else:
        return redirect(reverse('loginPage'))

    paginator = Paginator(story_list, 20)
    page = request.GET.get('page')
    try:
        story_ls = paginator.page(page)
    except PageNotAnInteger:
        story_ls = paginator.page(1)
    except EmptyPage:
        story_ls = paginator.page(paginator.num_pages)

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'stories' : story_ls,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'listing/pplist.html', context)


def toplists(request, cat):
    # most popular posts list.
    if cat == 'mystery':
        stories = Story.objects.filter(category='Mysterious').order_by('-popularity')
        cat_name = 'Mysterious'
    elif cat == 'weirdests':
        stories = Story.objects.all().order_by('-popularity')
        cat_name = 'Weirdests'
    elif cat == 'fun':
        stories = Story.objects.filter(category='Funny').order_by('-popularity')
        cat_name = 'Funny'

    paginator = Paginator(stories, ppp)
    page = request.GET.get('page')
    try:
        story_list = paginator.page(page)
    except PageNotAnInteger:
        story_list = paginator.page(1)
    except EmptyPage:
        story_list = paginator.page(paginator.num_pages)

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'stories' : story_list,
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'listing/toplist.html', context)


def report(request, urlcode):
    # report post form
    qs = get_object_or_404(Story, urlcode=urlcode)
    title = qs.title
    reportid = qs.urlcode
    form = ReportStory()

    if request.method == 'POST':
        form = ReportStory(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.story = qs
            obj.save()
            messages.success(request, "You have reported the post successfully. Thanks for your report!")
        else:
            messages.error(request, "Something went wrong. Try again please!")

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'post_title' : title,
        'reportid' : reportid,
        'form' : form,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'forms/report.html', context)


@login_required(redirect_field_name='redirect', login_url='/login')
def deleteconfirm(request, shortcode):
    # confirmation for delete process
    post = get_object_or_404(Story, urlcode=shortcode)
    if not post.author == request.user:
        messages.warning(request, "You are not authorised for deleting the post.")
        return redirect(reverse('storyPage', kwargs={'shortcode': shortcode}))

    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'post' : post,
        'notifications' : notifications,
        'unread' : unread,
    }
    return render(request, 'misc/delete_post.html', context)


@login_required(redirect_field_name='redirect', login_url='/login')
def deletepost(request):
    # delete post
    if request.method == 'POST':
        form = request.POST
        confirmcheck = form.get('confirm')
        shortcode = form.get('shortcode')
        qs = get_object_or_404(Story, urlcode=shortcode)
        if confirmcheck == 'confirmed' and qs:
            qs.delete()
            messages.success(request, 'Successfully deleted the story from the database!')
        else:
            messages.warning(request, 'You need to confirm!')
            return redirect(reverse('deleteconfirmPage', kwargs={'shortcode': shortcode}))
    return redirect(reverse('mypostsPage'))


class StoryVote(View):
    # this class-based view is for ajax requests for vote buttons
    def get(self, request, shortcode, *args, **kwargs):
        # retreive users vote data
        # return them as true/false
        # return as json response (urlcode, voted_down, voted_up)
        story_vote = {}
        story = Story.objects.get(urlcode=shortcode)
        qs_up = StoryUpvotes.objects.filter(
            Q(user=self.request.user) &
            Q(story=story))
        voted_up = qs_up.exists()
        story_vote['voted_up'] = voted_up

        qs_down = StoryDownvotes.objects.filter(
            Q(user=self.request.user) &
            Q(story=story))
        voted_down = qs_down.exists()
        story_vote['voted_down'] = voted_down
        story_vote['urlcode'] = shortcode

        return JsonResponse(story_vote)

    def post(self, request, shortcode, *args, **kwargs):
        #post request for upvote-model update
        response = {}
        story = Story.objects.get(urlcode=shortcode)

        # checking authentication status
        if self.request.user.is_authenticated:
            response['auth'] = True
            vote = request.POST.get('bttn')
            # if button-up is pressed then do the following
            if vote == 'button-up':
                qs_up = StoryUpvotes.objects.filter(
                    Q(user=self.request.user) &
                    Q(story=story))
                # if there is an upvote in db already, then don't do anything
                if qs_up.exists():
                    response['resp_code'] = 'exists'
                # if user haven't upvoted already, delete downvote if there is one then create upvote
                else:
                    try:
                        qs_down = StoryDownvotes.objects.filter(
                            Q(user=self.request.user) &
                            Q(story=story))
                        voted_down = qs_down.exists()
                        # if there is downvote, delete it
                        if voted_down:
                            qs_down.delete()
                        # create a new upvote object
                        StoryUpvotes.objects.create(user=self.request.user, story=story)
                        response['resp_code'] = 'upvoted'
                    except:
                        response['resp_code'] = 'error'
            # if button-down is pressed then do the following
            elif vote == 'button-down':
                qs_down = StoryDownvotes.objects.filter(
                    Q(user=self.request.user) &
                    Q(story=story))
                # if there is an downvote in db already, then don't do anything
                if qs_down.exists():
                    response['resp_code'] = 'exists'
                else:
                    try:
                        qs_up = StoryUpvotes.objects.filter(
                            Q(user=self.request.user) &
                            Q(story=story))
                        voted_up = qs_up.exists()
                        # if there is upvote, delete it
                        if voted_up:
                            qs_up.delete()
                        # create a new downvote object
                        StoryDownvotes.objects.create(user=self.request.user, story=story)
                        response['resp_code'] = 'downvoted'
                    except:
                        response['resp_code'] = 'error'
        #if authentication is not passed
        else:
            response['auth'] = False
        return JsonResponse(response)


class CommentVote(View):

    def get(self, request, shortcode, *args, **kwargs):
        commentlikes = []
        story = Story.objects.get(urlcode=shortcode)
        comments = story.storycomment_set.all()
        for comment in comments:
            count = comment.commentlike_set.filter(user=self.request.user)
            if count:
                commentlikes.append(comment.pk)
            #comment_like[comm.pk] = comm.commentlike_set.count

        return JsonResponse(commentlikes, safe=False)

    def post(self, request, shortcode, *args, **kwargs):
        # post request for comment like button
        response = {}
        story = Story.objects.get(urlcode=shortcode)
        compk = self.request.POST.get("compk")
        if self.request.user.is_authenticated:
            comment = StoryComment.objects.get(id=compk)
            user = self.request.user
            complike = CommentLike.objects.filter(comment=comment, user=user)

            if complike.exists():
                complike.delete()
                response["resp"] = "removed"
            else:
                CommentLike.objects.create(user=user, comment=comment)
                response["resp"] = "created"
        else:
            response['resp'] = 'auth_error'
        return JsonResponse(response)
