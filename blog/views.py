from django.views.generic import (ListView,
                                  DeleteView,
                                  CreateView,
                                  UpdateView,
                                  DetailView)
from django.contrib.auth.mixins import(LoginRequiredMixin,  #It is used for updating the post
                                       UserPassesTestMixin)  # Current loged in user can change only his own post. If others 403 forbidden.

from django.shortcuts import render
from django.http import Http404
from .models import Post
from .serializers import PostSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (generics,
                            mixins,
                            )

class PostGenericAPIView(generics.GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class PostGenericDetailAPIView(generics.GenericAPIView,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self,request,pk):
        return self.retrieve(request,pk)

    def put(self,request,pk):
        return self.update(request,pk)

    def delete(self,request,pk):
        return self.destroy(request,pk)




def home(request):
    posts=Post.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = '2'

class PostDetailView(DeleteView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def valid_form(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

                                        # Updating the form
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def valid_form(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = 'blog-home'

    def test_func(self):
        post= self.get_object()
        if self.request.user==post.author:
            return True
        return False