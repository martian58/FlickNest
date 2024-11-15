# movies/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def star_color(movie, user):
    return 'text-yellow-400' if movie in user.profile.starred_movies.all() else 'text-white'


@register.filter
def youtube_embed_link(value):
    return value.replace("watch?v=", "embed/")



