from django.urls import path
from .views import *

urlpatterns = [
    #Urls
    path('', index_view, name='index'),
    path('how_it_works', how_view, name='how'),
    path('feed/', home_view, name='home'),
    path('search/', search_posts, name='search_posts'),
    path('profile/', profile_view, name='profile'),
    path('profile/<str:type>/<str:name>', posts_by_something, name='posts-f'),
    path('comments/<int:post_id>', comments_view, name='comments'),
    path('messages/<str:username>', messages_view, name='messages'),
    path('conversations/', chat_list_view, name='chats'),
    path('update-profile/', update_profile, name='update_profile'),
    path('hug-post/', hug_post, name='hug_post'),


    #Authentication
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
]

handler404 = 'pages.views.handler404'
handler500 = 'pages.views.handler500'
handler403 = 'pages.views.handler403'
handler400 = 'pages.views.handler400'