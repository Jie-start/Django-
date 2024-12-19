from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Post
from .forms import UserRegistrationForm, PostForm
from taggit.models import Tag

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功！')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

def post_list(request):
    tag_slug = request.GET.get('tag')
    query = request.GET.get('q')
    posts = Post.objects.all()
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(summary__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    tags = Tag.objects.all()
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'tags': tags,
        'current_tag': tag_slug,
        'query': query
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    related_posts = Post.objects.filter(tags__in=post.tags.all()).exclude(id=post.id).distinct()[:3]
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'related_posts': related_posts
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # 保存标签
            messages.success(request, '文章创建成功！')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': '写新文章'})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, '您没有权限编辑这篇文章！')
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, '文章更新成功！')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': '编辑文章'})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, '您没有权限删除这篇文章！')
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, '文章删除成功！')
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
