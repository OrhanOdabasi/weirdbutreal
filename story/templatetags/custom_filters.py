from django import template

# Custom template tags

register = template.Library()

@register.filter
def upvote_count(vote_list):
    # returns upvotes count
    upvote_list = vote_list.filter(vote="Upvote")
    upvote_count = upvote_list.count()
    return upvote_count

@register.filter
def downvote_count(vote_list):
    # returns downvotes count
    downvote_list = vote_list.filter(vote="Downvote")
    downvote_count = downvote_list.count()
    return downvote_count
