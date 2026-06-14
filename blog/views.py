from django.http import JsonResponse, Http404
from django.shortcuts import render, reverse, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST,require_GET

from blog.forms import PubBlogForm
from blog.models import BlogCategory, Blog, BlogComment
from django.db.models import Q

def index(request):
    blogs = Blog.objects.all()

    return render(request, 'index.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        raise Http404
    return render(request, 'blog_detail.html', {'blog': blog})


# @login_required(login_url=(reverse_lazy('myauth:login')))
@login_required()
@require_http_methods(['GET', 'POST'])
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context={'categories': categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            print(content)
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            print('blog------------------------------', blog)
            return JsonResponse({'code': 200, 'message': "博客发布成功！", "data": {'blog_id': blog.id}})
        else:
            print(form.errors)
            return JsonResponse({'code': 400, 'message': "参数错误！"})
@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content=request.POST.get('content')
    BlogComment.objects.create(blog_id=blog_id, content=content,author=request.user)
    #重新加载博客详情页面
    return redirect(reverse('blog:blog_detail', kwargs={'blog_id': blog_id}))


@require_GET
def search(request):
    #通过/search?q=xxx搜索博客
    q = request.GET.get('q')
    #从博客的标题和内容中查找含有q关键字的博客
    blogs =  Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).all()
    return render(request,'index.html',context={'blogs':blogs})






















