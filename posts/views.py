from django.db.models import Count, Q
from django.views.generic import ListView, CreateView #DetailView
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.shortcuts import render, reverse, get_object_or_404, redirect
from .models import Post, Author
from marketing.models import Signup
from .forms import CommentForm, PostForm, UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
    'queryset': queryset,
    }
    return render(request, 'search_results.html', context)



def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset

#@login_required(redirect_field_name='login_page', login_url='/')
def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest,
    }
    return render(request, 'index.html', context)

@login_required(redirect_field_name='login_page', login_url='/login')
def blog(request):
    category_count = get_category_count()
    print(category_count)
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset' : paginated_queryset,
        'most_recent' : most_recent,
        'page_request_var' : page_request_var,
        'category_count' : category_count,
    }
    return render(request, 'blog.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'queryset post_list'

#class PostDetailView(DetailView):


#@login_required(redirect_field_name='login_page', login_url='/login')
def post(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post_detail", kwargs={
                'id': post.id
            }))
    context = {
        'form' : form,
        'most_recent' : most_recent,
        'category_count' : category_count,
        'post': post,
    }
    return render(request, 'post.html', context)

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post_detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

@login_required(redirect_field_name='login_page', login_url='/login')
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'overview', 'content', 'thumbnail', 'categories']
    def form_valid(self, form):
        form.instance.author = self.request.user




@login_required(redirect_field_name='login_page', login_url='/login')
def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post_detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

@login_required(redirect_field_name='login_page', login_url='/login')
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post_list"))

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/blog')

    context = {
    'form': form,
    }
    return render(request, 'login.html', context)

#def register_view(request):
#    next = request.GET.get('next')
#    form = UserRegisterForm(request.POST or None)
#    if form.is_valid():
#        user = form.save(commit=False)
#        password = form.cleaned_data.get('password')
#        user.set_password(password)
#        user.save()
#        new_user = authenticate(username=user.username, password=password)
#        login(request, new_user)
#        if next:
#            return redirect(next)
#        return redirect('/blog')
#
#    context = {
#    'form': form,
#    }
#    return render(request, 'signup.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created !')
            return redirect('/login')
    else:
        form = UserRegisterForm()
    context = {
        'form':form
    }
    return render(request, 'signup.html', context)


@login_required(redirect_field_name='login_page', login_url='/login')
def profile(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    return redirect('/login')
