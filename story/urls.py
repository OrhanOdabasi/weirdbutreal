from django.conf.urls import url
from story import views
from story.views import StoryVote, CommentVote


urlpatterns = [
    url(r'^$', views.homepage, name='homePage'),
    url(r'^weirdests/$', views.homepage, name='weirdestPage'),
    url(r'^funny/$', views.funny, name='funnyPage'),
    url(r'^mystery/$', views.mysterious, name='mysteriousPage'),
    url(r'^notifications/$', views.notifications, name='notificationsPage'),
    # url(r'^myprofile/$', views.profile, name='profilePage'),
    url(r'^help/$', views.help, name='helpPage'),
    url(r'^about/$', views.about, name='aboutPage'),
    url(r'^story/(?P<shortcode>[\w]+)$', views.story, name='storyPage'),
    url(r'^add/story/$', views.submitstory, name='storyFormPage'),
    url(r'^login$', views.login_view, name='loginPage'),
    url(r'^logout$', views.logout_view, name='logoutPage'),
    url(r'^register$', views.register, name='registerPage' ),
    url(r'^pass-reminder/$', views.passReminder, name='passreminderPage'),
    url(r'^myposts$', views.myposts, name='mypostsPage'),
    url(r'^mycomments$', views.mycomments, name='mycommentsPage'),
    url(r'^myupvotes$', views.myupvotes, name='myupvotesPage'),
    url(r'^mydownvotes$', views.mydownvotes, name='mydownvotesPage'),
    url(r'^search$', views.searchpost, name='searchPage'),
    url(r'^edit-profile', views.editprofile, name='editprofilePage'),
    url(r'^profile/(?P<profile>[a-zA-Z0-9_]+)/postlist$', views.profilepostlist, name='pplistPage'),
    url(r'^top/(?P<cat>[a-z]+)/', views.toplists, name='toplistPage'),
    url(r'^report/(?P<urlcode>[\w]+)/$', views.report, name='reportPage'),
    url(r'^delete-confirm/(?P<shortcode>[\w]+)$',views.deleteconfirm, name='deleteconfirmPage'),
    url(r'^delete-post/$', views.deletepost, name='deletePage'),
    url(r'^ajax/storyvote/(?P<shortcode>[\w]+)/$', StoryVote.as_view(), name="ajaxstoryvote"),
    url(r'^ajax/commentvote/(?P<shortcode>[\w]+)/$', CommentVote.as_view(), name="ajaxcommentvote"),

]
