from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .serializer import *
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from rest_framework import viewsets

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)



#To do list View
class TodoListView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        todo = Todo.objects.filter(user=user)
        print(user)
        return todo


#To do delete retrive and upadate view
class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']

        user = User.objects.get(id=user_id)
        todo = Todo.objects.get(id=todo_id, user=user)

        return todo

#To do mark complete
class TodoMarkAsCompleted(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']

        user = User.objects.get(id=user_id)
        todo = Todo.objects.get(id=todo_id, user=user)

        todo.completed = True
        todo.save()

        return todo

#stats todo

class TodoSummaryView(APIView):
    def get(self, request, user_id):
        total_tasks = Todo.objects.filter(user_id=user_id).count()
        active_tasks = Todo.objects.filter(user_id=user_id, completed=False).count()
        completed_tasks = Todo.objects.filter(user_id=user_id, completed=True).count()

        return Response({
            'total_tasks': total_tasks,
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks
        })


####Blogs functionality start

class BlogListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 10

#Blogs List
class BlogList(ListAPIView):
    queryset = Blogs.objects.all().order_by('-date')
    serializer_class = BlogViewSerializer
    pagination_class = BlogListPagination

#Single Blog view
from urllib.parse import unquote

class BlogView(generics.ListAPIView):
    serializer_class = BlogViewSerializer

    def get_queryset(self):
        # Get the blog title from the URL kwargs and decode it
        encoded_title = self.kwargs.get('url')
        blog_url = unquote(encoded_title)

        # Fetch the blog post using the decoded title and update the views
        blog = get_object_or_404(Blogs, url=blog_url)
        blog.views += 1
        blog.save()

        # Return a queryset with the single blog instance
        return Blogs.objects.filter(url=blog_url)


#Blogs List
class BlogIndex(ListAPIView):
    queryset = Blogs.objects.all().order_by('-date')
    serializer_class = BlogViewSerializer


#Get blog comments
def get_blog_comments(request, url):
    try:
        # Decode the title from URL encoding
        decoded_url = unquote(url)

        # Fetch the blog by its title
        blog = get_object_or_404(Blogs, url=decoded_url)

        # Fetch the comments related to the blog
        blog_comments = Comment.objects.filter(blog=blog)
        serializer = CommentGetSerializer(blog_comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Blogs.DoesNotExist:
        return JsonResponse({'error': 'Blog not found.'}, status=404)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comments not found for this blog.'}, status=404)



#Post comments
class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, blog_id):
        data = request.data.copy()
        data['user'] = request.user.id
        data['blog'] = blog_id
        data['username'] = request.user.username  # Add username to the data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Print errors to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



## add blog
class BlogPostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Assign the logged-in user to the post
        print(data)
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##blog functionality end


#Language
class LanguageLists(generics.ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer



class TopicsView(generics.ListCreateAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        lang_url = self.kwargs['url']
        language = generics.get_object_or_404(Language, url=lang_url)
        topics = Topics.objects.filter(language=language)
        return topics



class CodeView(generics.ListCreateAPIView):
    serializer_class = CodeSerializer

    def get_queryset(self):
        code_url = self.kwargs['url']
        topic = generics.get_object_or_404(Topics, url=code_url)
        return CodeSnippet.objects.filter(topic=topic)

#single code view
class CodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CodeSnippet.objects.all()
    serializer_class = CodeSerializer
    lookup_field = 'url'


#Tutorials list view
class TutorialList(generics.ListCreateAPIView):
    queryset = TutorialName.objects.all()
    serializer_class = TutorialNameSerializer


#Each Tutorial view
class TutorialDetail(generics.ListCreateAPIView):
    serializer_class = TutorialPostSerializer

    def get_queryset(self):
        tutorial_url = self.kwargs['url']
        tutorial = generics.get_object_or_404(TutorialName, url=tutorial_url)
        return TutorialPost.objects.filter(tutorialName=tutorial)

#List of each Tutorial Topics
class PostView(generics.ListAPIView):
    queryset = TutorialPost.objects.all()
    serializer_class = TutorialPostSerializer

    def get_queryset(self):
        url = self.kwargs['url']

        post = TutorialPost.objects.filter(url=url)
        return post

#List of Post view
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TutorialPost.objects.all()
    serializer_class = TutorialPostSerializer
    lookup_field = 'url'


class TutorialCommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, url):
        data = request.data.copy()
        data['user'] = request.user.id
        data['post'] = url
        data['username'] = request.user.username  # Add username to the data
        serializer = TutorialCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Print errors to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_post_comments(request, url):
    try:
        post_comments = Comment_tutorials.objects.filter(url=url)
        serializer = CommentGetTutSerializer(post_comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comments not found for this blog.'}, status=404)



#Blog Post and delete view
class BlogPostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Assign the logged-in user to the post
        print(data)
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#Loggedin user Blogs
class BlogsUserListView(generics.ListCreateAPIView):
    queryset = Blogs.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        blog = Blogs.objects.filter(user=user)
        return blog

#Single blog view of user
class BlogsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogViewSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        blog_id = self.kwargs['blog_id']

        user = User.objects.get(id=user_id)
        blog = Blogs.objects.get(id=blog_id, user=user)

        return blog



def search_blog(request):
    query = request.GET.get('query', '')
    results = Blogs.objects.filter(url__icontains=query)

    # Serialize the blog data
    data = []
    for result in results:
        blog_data = {
            'title': result.title,
            'content': result.content,
            'id': result.id,
            'views': result.views,
            'date': result.date,
            # Serialize user as a dictionary
            'user': {
                'id': result.user.id,
                'username': result.user.username,
                'email': result.user.email,  # Include any other user fields you need
            }
        }
        data.append(blog_data)

    return JsonResponse(data, safe=False)

def search_code(request):
    query = request.GET.get('query', '')
    results = CodeSnippet.objects.filter(url__icontains=query)

    # Serialize the code snippet data
    data = []
    for result in results:
        snippet_data = {
            'title': result.title,
            'content': result.content,
            'code_id': result.code_id,
            'code': result.code,
            # Assuming there's an 'author' field which is a foreign key to the User model
            'user': {
                'id': result.user.id,
                'username': result.user.username,
                'email': result.user.email,  # Include other necessary fields
            } if hasattr(result, 'user') and result.user else None
        }
        data.append(snippet_data)

    return JsonResponse(data, safe=False)



#problem Post and delete view
class ProblemPostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Assign the logged-in user to the post
        print(data)
        serializer = ProblemSolveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def contact_handler(request):
    if request.method == "POST":
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Send email to user
            subject = 'THANK YOU FOR CONTACTING ME'
            html_content = render_to_string('contact_html.html', {'name': serializer.data["name"]})
            text_content = strip_tags(html_content)  # Strip the html tag
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [serializer.data["email"]]
            msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # Send email notification to owner
            subject1 = 'HELLO SIR, YOU GOT A NEW MAIL'
            message1 = f'Hi k satyanarayana chary, Someone contacted you details are:- \nUsername: {serializer.data["name"]},\nEmail: {serializer.data["email"]},\nSubject: {serializer.data["subject"]},\nMessage: {serializer.data["message"]} \n'
            email_from = settings.EMAIL_HOST_USER
            recipient_list1 = ['acadamicfolio@gmail.com']
            send_mail(subject1, message1, email_from, recipient_list1)

            return Response({'message': 'Thanks for contacting me. I will look forward to utilizing this opportunity.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShortListCreateView(generics.ListCreateAPIView):
    queryset = Short.objects.all().order_by('-created_at')
    serializer_class = ShortSerializer

@require_GET  # Ensures the view only responds to GET requests
def get_latest_update(request):
    # Fetch the latest update by ordering by date and taking the first result
    latest_update = Latest_update.objects.order_by('-date').first()

    if latest_update:
        # Serialize the latest update to JSON
        data = {
            'update': latest_update.update,
            'date': latest_update.date,
        }
    else:
        # If there are no updates, return a message
        data = {
            'error': 'No updates found',
        }

    return JsonResponse(data)


# Language Views
class LanguageList(generics.ListCreateAPIView):
    queryset = LanguageMcq.objects.all()
    serializer_class = LanguageMcqSerializer

class LanguageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LanguageMcq.objects.all()
    serializer_class = LanguageMcqSerializer

# Topic Views
class TopicList(generics.ListCreateAPIView):
    queryset = TopicMcq.objects.all()
    serializer_class = TopicMcqSerializer

class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TopicMcq.objects.all()
    serializer_class = TopicMcqSerializer

# Question Views
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# Option Views
class OptionList(generics.ListCreateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

class OptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

# Result Views
class ResultList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class ResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer




class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ShortListView(generics.ListAPIView):
    serializer_class = ShortSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            return Short.objects.filter(category_id=category_id)
        return Short.objects.all()

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#Blog Post and delete view
class ProfilePostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Assign the logged-in user to the post
        print(data)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def reset_password_confirm(request, uid, token):
    return redirect(f"https://acadamicfolio.info/reset/password/confirm/{uid}/{token}")