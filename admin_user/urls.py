from django.urls import *
from .views import *


# Custom 404 error view
handler404 = 'admin_user.views.error_404' 
# Custom 500 error view
handler500 = 'admin_user.views.error_500' 

urlpatterns = [
    path('',index,name="index"),
    path('login/',Login,name='login'),
    path('homepage/',home,name='homepage'),
    path('logout/',logout_view,name='logout'),
    path('post_meme/',MemePostCreateView,name='post_meme'),
    path('post_blog/',create_blog,name='post_blog'),
    path('post_code/',CodePostCreateView,name='post_code'),
    path('add_topic/', add_topic, name='add_topic'),
    path('add_language/', create_language, name='add_language'),
    path('add_post/', TutorialTopicCreateView, name='add_post'),
    path('add_tutorial/', create_tutorial, name='add_tutorial'),
    path('blogs/<int:id>/',blogSingle),
    path('codes/<int:code_id>/',CodeSingle),
    path('topics/<int:post_id>/',topicSingle),
    path('memes/<int:id>/',MemeSingle),
    path('user_detail/', admin_user_detail, name='admin_user_detail'),
    path('user_password_change/', admin_user_password_change, name='admin_user_password_change'),
    path('profile/', profile, name='profile'),
    
    

]