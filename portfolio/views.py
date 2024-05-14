from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post, Category
# from .models import Comment
from .forms import NewCommentForm
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import JsonResponse
from taggit.models import Tag


def home(request):

    all_posts = Post.newmanager.all()
    
    # pagination
    paginator = Paginator(all_posts, 10)  # 10 posts per page

    page = request.GET.get('page')
    try:
        steps = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        steps = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        steps = paginator.page(paginator.num_pages)

    return render(request, 'portfolio/index.html', {'posts': all_posts, 'steps':steps})


def post_single(request, post):

    post = get_object_or_404(Post, slug=post, status='published')

    comments = post.comments.filter(status=True)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post.slug)
    else:
        comment_form = NewCommentForm()
        
    context = {
        'post': post, 
        'comments':  user_comment, 
        'comments': comments, 
        'comment_form': comment_form
        }
    return render(request, 'portfolio/single.html', context)

def tags_list(request, tag_slug=None):
    posts = Post.newmanager.filter(status='published').order_by('-publish')
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.newmanager.filter(tags__in=[tag])
        
    context = {
        'posts':posts,
        'tag':tag
    }
    
    return render(request, 'portfolio/tags.html', context)


class CatListView(ListView):
    template_name = 'portfolio/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published')
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context



def search_view(request):
    query = request.GET.get('q')
    posts = Post.newmanager.filter(title__icontains=query, content__icontains=query).order_by('-publish')
    context = {
        'query':query,
        'posts':posts,
    }
    return render(request, 'portfolio/search.html', context)
    


def about(request):
    return render(request, 'portfolio/about.html')

def contact(request):
    return render(request, 'portfolio/contact.html')