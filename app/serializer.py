from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # These are claims, you can add custom claims
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        token['image'] = str(user.profile.image)
        token['gitlink'] = user.profile.gitlink

        # ...
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']

        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'completed']

class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blogs
        fields = ['id', 'user', 'title', 'content', 'date', 'likes','views','url']


class BlogViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Blogs
        fields = ['id', 'user', 'title', 'content', 'date', 'likes','views','url']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['blog', 'user', 'date', 'content']

class CommentGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ['blog', 'user', 'date', 'content']

class CodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodeSnippet
        fields = ['code_id', 'title', 'code', 'content', 'topic','url']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'language','url']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['id','topic','url']


class TutorialNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialName
        fields = ['id', 'tutorialName', 'tutorialContent', 'tutorialImage','url']


class TutorialPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialPost
        fields = ['post_id', 'post_title', 'post_content', 'post_file', 'tutorialName', 'post_video','url']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['blog', 'user', 'date', 'content']

class TutorialCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_tutorials
        fields = ['post', 'user', 'date', 'content']

class CommentGetTutSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment_tutorials
        fields = ['post', 'user', 'date', 'content']

class ProblemSolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem_solve
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Short
        fields = '__all__'


class LanguageMcqSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageMcq
        fields = '__all__'

class TopicMcqSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicMcq
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ShortSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Short
        fields = ['id', 'title', 'video_url', 'description', 'created_at', 'views', 'category']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'role', 'gitlink', 'image']

