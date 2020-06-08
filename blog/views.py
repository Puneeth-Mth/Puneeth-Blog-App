from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# to many to import then keep in tuple(....,.....)
from django.views.generic import (ListView,DetailView,CreateView,DeleteView,UpdateView,DeleteView)
#generic view in bulit present django
# ListView is used to list all the blod post of that user
# like =blog post,listing all subscriber at one place
# detailView ...etc


# Create your views here.

def home(request):
	context={'posts':Post.objects.all()}
	return render(request,'blog/home.html',context)

# class based View
class PostListView(ListView):
	model=Post
	template_name='blog/home.html'
	# by default ListView looks at this path --> blog/post_list.html
	# was ListView by default it calls objectList---our object is 
	# posts---> present context
	context_object_name='posts'
	ordering=['-date_posted'] #desecending order use - sign like -1 in slicing
	paginate_by=5 #one page can 5 post are displayed

#author or user of the post then we will is print all post related to the author
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model=Post


# LoginRequiredMixin --> try to access post/new/ directly without login
# then it will redirect to login apge
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
    	# we are saying--> login details to current author to create new post
        form.instance.author = self.request.user
        return super().form_valid(form)
        # we are over riding this form_vaild() present in CreateView
 		# so that to avoid interity error saying that use the form details 
 		# for that author

# UserPassesTestMixin if we use to this random user cant edit the post 
# there can edit only there post /post/6/update only authenicated user can edit
class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
    	# we are saying--> login details to current author to create new post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
    	post=self.get_object()
    		# current login user==authenicated user -->>edit the post
    	if self.request.user == post.author:
    		return True
    	else:
    		return False



class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model=Post
	success_url='/' #after deleting goto this route.

	def test_func(self):
		post=self.get_object()
		# current login user==authenicated user -->>edit the post
		if self.request.user == post.author:
			return True
		else:
			return False

def about(request):
	return render(request,'blog/about.html',{'title':'About'})

