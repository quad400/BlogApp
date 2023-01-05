from rest_framework import authentication, permissions, generics,status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist

from core.permissions import IsOwnerOrReadOnly
from core.authentication import TokenAuthentication
from .serializers import BlogSerializer,BlogCommentSerializer
from .models import Blog,BlogComment

class BlogListAPI(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
        ]
    queryset = Blog.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        result = Blog.objects.all()
        if q is not None:
            result = qs.by_category(q)
        return result


class BlogCreateAPI(generics.CreateAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
        ]

    def perform_create(self, serializer):
        serializer.save(post_user=self.request.user)


class BlogDetailAPI(generics.RetrieveAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
        ]


class BlogUpdateAPI(generics.UpdateAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field='slug'
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAdminUser]
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
        ]



class BlogDeleteAPI(generics.DestroyAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field='slug'
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAdminUser]
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
        ]


class BlogLikesAPI(generics.CreateAPIView):

    serializer_class = BlogSerializer
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        slug = kwargs["slug"]
        qs = Blog.objects.filter(slug=slug)
        if not qs.exists():
            return Response({"detail": "Blog not found"}, 
                                    status=status.HTTP_404_NOT_FOUND)
        obj = qs.first()
        data = request.data or {}
        action = data.get("action")
        user = request.user
           
        if not user in obj.likes.all():
            if action == "like":
                obj.likes.add(user)
            else:
                return Response({f"{action} is not a valid action"}, status=status.HTTP_400_BAD_REQUEST)
        
        elif user in obj.likes.all():
            if action == "unlike":
                obj.likes.remove(user)
            else:
                return Response({f"{action} is not a valid action"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=obj, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        action = self.request.get("action")
        return super().get_object()


class BlogCommentCreateListAPI(APIView):

    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs['slug']
        qs = Blog.objects.filter(slug=slug)

        if not qs.exists():
            return Response('Blog not found', status=status.HTTP_404_NOT_FOUND)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, format=None, *args, **kwargs):
        slug = kwargs['slug']
        try:
            serializer = BlogCommentSerializer(data=request.data)
            if serializer.is_valid():
                comment = serializer.validated_data.pop('comment')
                blog = Blog.objects.get(slug=slug)
                if request.user.is_authenticated:
                    blog_comment = BlogComment.objects.create(user=request.user,comment=comment,blog=blog)
                    serializer.save(blog_comment)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response('User must be authenticated', status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response('Blog not found', status=status.HTTP_404_NOT_FOUND)

        except:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, format=None, *args, **kwargs):
        slug = kwargs['slug']

        try:
            comment = BlogComment.objects.filter(blog__slug=slug)
            serializer = BlogCommentSerializer(comment,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response('Internal server error', 
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)