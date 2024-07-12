from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'profile', ProfileViewSet)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('test/', testEndPoint, name='test'),
    path('', getRoutes),

    path("todo/<user_id>/", TodoListView.as_view()),
    path("todo-detail/<user_id>/<todo_id>/", TodoDetailView.as_view()),
    path("todo-mark-as-completed/<user_id>/<todo_id>/", TodoMarkAsCompleted.as_view()),
    path('todos/<int:user_id>/summary/', TodoSummaryView.as_view(), name='todo_summary'),

    path('blogs/', BlogList.as_view(), name='blog-list'),
    path('blogsindex/', BlogIndex.as_view(), name='blog-index'),
    path("blogs/<str:url>/",BlogView.as_view(), name='blog'),
    path("blog/<user_id>/", BlogsUserListView.as_view()),
    path("blog/<user_id>/<blog_id>/", BlogsDetailView.as_view()),
    path('blogs/<str:url>/comments/', get_blog_comments, name='get_blog_comments'),
    path('post-blog/', BlogPostCreateView.as_view(), name='post-blog'),
    path('blog/<str:url>/comment/create/', CommentCreateView.as_view(), name='comment_create'),

    path('languages/', LanguageLists.as_view(), name='languages-list'),
    path('languages/<str:url>/topics/', TopicsView.as_view(), name='topics-details'),
    path('languages/<str:url>/codes/', CodeView.as_view(), name='code-details'),
    path('languages/codes/<str:url>/', CodeDetail.as_view(), name='code-detailsview'),

    path('tutorials/', TutorialList.as_view(), name='Tutorials-list'),
    path('tutorials/<str:url>/', TutorialDetail.as_view(), name='tutorial-detail'),
    path('post/<str:url>/', PostView.as_view(), name='post-details'),
    path('tutorials/<str:url>/comments/', get_post_comments, name='get_blog_comments1'),
    path('tutorials/posts/<str:url>/', PostDetail.as_view(), name='post-detailsview'),
    path('tutorials/<str:url>/comment/create/', TutorialCommentCreateView.as_view(), name='comment_create1'),

    path('post-problem/', ProblemPostCreateView.as_view(), name='problem-blog'),

    path('search/', search_blog, name='search_model'),
    path('search_code/',search_code, name='search_model'),
    path('shorts/', ShortListCreateView.as_view(), name='shorts-list-create'),
    path('latest-update/', get_latest_update, name='latest-update'),

     # Language URLs
    path('languageMcq/', LanguageList.as_view(), name='language-list'),
    path('languagesMcq/<int:pk>/', LanguageDetail.as_view(), name='language-detail'),

    # Topic URLs
    path('topicsMcq/', TopicList.as_view(), name='topic-list'),
    path('topicsMcq/<int:pk>/', TopicDetail.as_view(), name='topic-detail'),

    # Question URLs
    path('questions/', QuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),

    # Option URLs
    path('options/', OptionList.as_view(), name='option-list'),
    path('options/<int:pk>/', OptionDetail.as_view(), name='option-detail'),

    # Result URLs
    path('results/', ResultList.as_view(), name='result-list'),
    path('results/<int:pk>/', ResultDetail.as_view(), name='result-detail'),

    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/shorts/', ShortListView.as_view(), name='short-list'),

    path('profile-post/', ProfilePostCreateView.as_view(), name='short-list'),

    path('api/', include(router.urls)),
]