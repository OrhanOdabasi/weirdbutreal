
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
from django.core.exceptions import ObjectDoesNotExist

from .models import (Story,
                    StoryComment,
                    Vote,
                    CommentLike,
                    Profile,
                    Notification,
                    Confirmation,
                    PasswordReset)
from .forms import (PostStoryForm,
                    LoginForm,
                    SignupForm,
                    SearchPostForm,
                    ProfileEditForm,
                    UserEditForm,
                    CommentForm,
                    ReportStoryForm,
                    ForgottenPasswordForm,
                    ChangePasswordForm,
                    ResetPasswordForm)

# post per page
ppp = 10

# entry per top menu
eptm = 5
def latestStories(eptm):
    # Create your views here.
    latest_f = Story.objects.filter(category="Funny", active=True).order_by("-popularity")[:eptm]
    latest_m = Story.objects.filter(category="Mysterious", active=True).order_by("-popularity")[:eptm]
    latest_a = Story.objects.filter(active=True).order_by("-popularity")[:eptm]
    return latest_f, latest_m, latest_a


def getNotifications(user, last):
    notifications = Notification.objects.filter(owner=user)
    unread = notifications.filter(read=False).count()
    notifications = notifications.order_by('-notify_time')[:last]
    return unread, notifications

# Views methods

def homepage(request):
    # Home Page
    stories = Story.objects.filter(active=True).order_by("-created")
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
    stories = Story.objects.filter(category='Funny', active=True).order_by("-modified")
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
    stories = Story.objects.filter(category='Mysterious', active=True).order_by("-modified")
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

# TODO: Undone profile system
"""
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
    qs = get_object_or_404(Story, urlcode=shortcode, active=True)
    comment_count = qs.storycomment_set.count()
    if qs.storycomment_set:
        # list comments
        comments = qs.storycomment_set.all().annotate(topvotes=Count('commentlike'))
        comments = comments.order_by('-topvotes', '-comment_date')
    else:
        comments = False

    commentform = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
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

@login_required(redirect_field_name='redirect', login_url='/login')
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


@login_required(redirect_field_name='redirect', login_url='/login')
def changepassword(request):
    # change password
    form = ChangePasswordForm()
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = request.POST.get("old_password")
            auth_check = authenticate(username=user, password=old_password)
            if auth_check:
                new_password = request.POST.get("new_password")
                try:
                    u = User.objects.get(username=user)
                    u.set_password(new_password)
                    u.save()
                    msg = "Your password has been changed successfully!"
                    messages.success(request, msg)
                except:
                    msg = "Some error occured!"
                    messages.warning(request, msg)
            else:
                msg = "Your old password did not match!"
                messages.warning(request, msg)

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
        'form' : form,
    }
    return render(request, 'forms/changepassword.html', context)


def forgottenpassword(request):
    # password reset page
    if request.user.is_authenticated:
        return redirect(reverse('profilePage'))
    form = ForgottenPasswordForm(request.POST or None)
    if form.is_valid():
        email_addr = request.POST.get("email_addr")
        user = User.objects.get(email=email_addr)
        have_key = PasswordReset.objects.filter(user=user)
        if not have_key:
            PasswordReset.objects.create(user=user)
            # A signal is sent for sending email
            msg = "We have sent you a mail. Please check your mailbox."
            msg1 = "It may take some time to be delivered. Don't panic:)"
            messages.success(request, msg+msg1)
        else:
            msg = "We have already sent you a password reset link! Check your mailbox again!"
            messages.warning(request, msg)

    latest_f, latest_m, latest_a = latestStories(eptm)

    context = {
        'latest_f' : latest_f,
        'latest_m' : latest_m,
        'latest_a' : latest_a,
        'notifications' : False,
        'unread' : False,
        'form' : form,
    }
    return render(request, 'registration/forgottenpassword.html', context)


@login_required(redirect_field_name='redirect', login_url='/login')
def myposts(request):
    # users' post list
    if request.user.is_authenticated:
        qs = get_object_or_404(User, username=request.user)
        story_list = qs.story_set.filter(active=True).order_by('-modified')
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
        my_upvotes = Vote.objects.filter(user=user, vote="Upvote")
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
        my_downvotes = Vote.objects.filter(user=user, vote="Downvote")
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
            Q(text__icontains=query)&
            Q(active=True)
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


@login_required(redirect_field_name='redirect', login_url='/login')
def editprofile(request):
    # edit your user profile
    qs = get_object_or_404(User, username=request.user)
    email_addr = qs.email # It's for checking email if it's changed
    qs2 = get_object_or_404(Profile, user=request.user)

    # display a message for unconfirmed accounts
    confirm_status = qs2.confirmed
    if not confirm_status:
        msg = "We sent you a confirmation mail. Please confirm your e-mail address. "
        msg1 = "It may take some time to be delivered. Don't panic:)"
        messages.warning(request, msg+msg1)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = UserEditForm(request.POST, instance=qs, prefix="formone")
            formtwo = ProfileEditForm(request.POST, instance=qs2, prefix="formtwo")

            if form.is_valid() and formtwo.is_valid() and confirm_status:
                email_field = request.POST.get("formone-email")
                if email_field != email_addr:
                    f = formtwo.save(commit=False)
                    f.confirmed = False
                    f.save()
                    Confirmation.objects.create(user=request.user)
                    msg = "You should confirm your e-mail to change you details!"
                    messages.warning(request, msg)
                else:
                    formtwo.save()
                form.save()
                messages.success(request, 'Your Profile has been updated successfully!')
            # User must not change details if account is not confirmed yet.
            elif not confirm_status:
                msg = "You should confirm your e-mail to change you details!"
                messages.warning(request, msg)

    form = UserEditForm(instance=qs, prefix="formone")
    formtwo = ProfileEditForm(instance=qs2, prefix="formtwo")


    latest_f, latest_m, latest_a = latestStories(eptm)
    if request.user.is_authenticated:
        unread, notifications = getNotifications(user=request.user, last=5)
    else:
        notifications = False
        unread = False

    context = {
        'form' : form,
        'formtwo': formtwo,
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
        story_list = qs.story_set.filter(active=True).order_by('-modified')
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
        stories = Story.objects.filter(category='Mysterious', active=True).order_by('-popularity')
        cat_name = 'Mysterious'
    elif cat == 'weirdests':
        stories = Story.objects.filter(active=True).order_by('-popularity')
        cat_name = 'Weirdests'
    elif cat == 'fun':
        stories = Story.objects.filter(category='Funny', active=True).order_by('-popularity')
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
        'cat_name' : cat_name,
    }
    return render(request, 'listing/toplist.html', context)


def report(request, urlcode):
    # report post form
    qs = get_object_or_404(Story, urlcode=urlcode, active=True)
    title = qs.title
    reportid = qs.urlcode
    form = ReportStoryForm()

    if request.method == 'POST':
        form = ReportStoryForm(request.POST)
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
    post = get_object_or_404(Story, urlcode=shortcode, active=True)
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
        qs = get_object_or_404(Story, urlcode=shortcode, active=True)
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
        # retrieve users vote data
        response = {}
        story = Story.objects.get(urlcode=shortcode, active=True)
        try:
            vote_status = Vote.objects.get(user=self.request.user, story=story)
            response["vote_status"] = vote_status.vote
        except ObjectDoesNotExist:
            response["vote_status"] = "DoesNotExist"
        return JsonResponse(response)

    def post(self, request, shortcode, *args, **kwargs):
        #post request for upvote-model update
        response = {}
        story = Story.objects.get(urlcode=shortcode, active=True)
        if self.request.user.is_authenticated:
            vote_req = self.request.POST.get("bttn")
            if vote_req == 'button-up':
                vote = "Upvote"
            elif vote_req == 'button-down':
                vote = "Downvote"
            user = self.request.user
            qs = Vote.objects.filter(user=user, story=story, vote=vote)
            if qs:
                response["response"] = "VotedAlready"
            else:
                defaults = {'vote' : vote}
                obj, created = Vote.objects.update_or_create(user=user, story=story, defaults=defaults)
                response["response"] = obj.vote
        else:
            response["response"] = "NotAuthenticated"
        return JsonResponse(response)


class CommentVote(View):

    def get(self, request, shortcode, *args, **kwargs):
        commentlikes = []
        story = Story.objects.get(urlcode=shortcode, active=True)
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
        story = Story.objects.get(urlcode=shortcode, active=True)
        compk = self.request.POST.get("compk")
        if self.request.user.is_authenticated:
            comment = StoryComment.objects.get(id=compk)
            user = self.request.user
            complike = CommentLike.objects.filter(comment=comment, user=user)

            if complike.exists():
                complike.first().delete()
                response["resp"] = "removed"
            else:
                CommentLike.objects.create(user=user, comment=comment)
                response["resp"] = "created"
        else:
            response['resp'] = 'auth_error'
        return JsonResponse(response)


@login_required(redirect_field_name='redirect', login_url='/login')
def removevotes(request):
    # removes the vote or like objects in profile menu
    datacat = request.POST.get("datacat")
    datacode = request.POST.get("datacode")
    user = request.user

    if datacat == 'storyupvote':
        story = Story.objects.filter(urlcode=datacode, active=True)
        try:
            q = Vote.objects.get(user=user, story=story, vote='Upvote')
        except:
            q = False
        if q: q.delete()
    elif datacat == 'storydownvote':
        story = Story.objects.filter(urlcode=datacode, active=True)
        try:
            q = Vote.objects.get(user=user, story=story, vote="Downvote")
        except:
            q = False
        if q: q.delete()
    elif datacat == 'comment':
        q = StoryComment.objects.get(pk=datacode, commentator=user)
        if q: q.delete()
    return HttpResponse("")


def confirmation(request, username, securekey):
    # Confirms the secure key
    user = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        # if another user is authenticated, redirect to profile edit page
        if request.user.username != user.username:
            messages.warning(request, "You can confirm your e-mail address only!")
        else:
            qs = Confirmation.objects.filter(user=user)
            if qs:
                c = Confirmation.objects.get(user=user)
                if securekey == c.key:
                    chng = Profile.objects.get(user=user)
                    chng.confirmed = True
                    chng.save()
                    messages.info(request, "You confirmed your e-mail successfully!")
                else:
                    messages.warning(request, "Confirmation key is invalid! Check your link, please!")
            else:
                messages.info(request, "Your account is already confirmed!")
        return redirect(reverse("editprofilePage"))
    else:
        p = Profile.objects.get(user=user)
        if p.confirmed:
            messages.info(request, "You account is already confirmed! You can login now!")
        if not p.confirmed:
            c = Confirmation.objects.get(user=user)
            if securekey == c.key:
                p.confirmed = True
                p.save()
                messages.info(request, "You confirmed your e-mail successfully! You can login now!")
            else:
                messages.warning(request, "Confirmation key is invalid! Check your link, please!")
        return redirect(reverse("homePage"))


def resetpassword(request, username, securekey):
    # reset user's password if the password is forgotten
    #redirect to usereditpage
    if request.user.is_authenticated:
        return redirect(reverse("editprofilePage"))
    else:
        user = get_object_or_404(User, username=username)
        passreset = PasswordReset.objects.filter(user=user, key=securekey)
        if passreset:
            form = ResetPasswordForm(request.POST or None)
            if form.is_valid():
                password = form.cleaned_data.get("new_password")
                user.set_password(password)
                user.save()
                passreset.delete()
                u = authenticate(username=user.username, password=password)
                login(request, u)
                messages.info(request, "You changed your password successfully!")
                return redirect(reverse("editprofilePage"))

            latest_f, latest_m, latest_a = latestStories(eptm)

            context = {
                'latest_f' : latest_f,
                'latest_m' : latest_m,
                'latest_a' : latest_a,
                'notifications' : False,
                'unread' : False,
                'form' : form,
            }
            return render(request, 'forms/resetpassword.html', context)
        else:
            messages.warning(request, "Your password reset key is invalid!")
            return redirect(reverse("resetpasswordPage"))
