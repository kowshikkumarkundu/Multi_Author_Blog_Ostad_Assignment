from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment, Like
from .forms import PostForm, CommentForm

def home_view(request):
    posts_list = Post.objects.filter(status='published')
    
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    search_query = request.GET.get('q')

    if category_slug:
        posts_list = posts_list.filter(category__slug=category_slug)
    if tag_slug:
        posts_list = posts_list.filter(tags__slug=tag_slug)
    if search_query:
        posts_list = posts_list.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )

    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Restrict draft visibility
    if post.status == 'draft':
        if not request.user.is_authenticated or (request.user != post.author and not request.user.is_superuser):
            raise PermissionDenied("You do not have permission to view this draft.")

    # Single-session view counter increment
    session_key = f"viewed_post_{post.id}"
    if not request.session.get(session_key, False):
        post.view_count += 1
        post.save(update_fields=['view_count'])
        request.session[session_key] = True

    comments = post.comments.all()
    comment_form = CommentForm()

    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(post=post, user=request.user).exists()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
    })

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment posted successfully.")
    return redirect('post_detail', slug=slug)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user == comment.post.author or request.user.is_superuser:
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect('post_detail', slug=comment.post.slug)
    else:
        raise PermissionDenied("You cannot delete this comment.")

@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('post_detail', slug=slug)

@login_required
def author_dashboard(request):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_author:
        raise PermissionDenied("Only authors can access the dashboard.")
    
    posts = Post.objects.filter(author=request.user)
    return render(request, 'author_dashboard.html', {'posts': posts})

@login_required
def create_post(request):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_author:
        raise PermissionDenied("Only authors can create posts.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "Post created successfully!")
            return redirect('author_dashboard')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form, 'action': 'Create'})

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_superuser:
        raise PermissionDenied("You can only edit your own posts.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('author_dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form, 'action': 'Edit'})

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_superuser:
        raise PermissionDenied("You can only delete your own posts.")

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('author_dashboard')
    return render(request, 'post_confirm_delete.html', {'post': post})

def author_profile(request, username):
    author_user = get_object_or_404(User, username=username)
    published_posts = Post.objects.filter(author=author_user, status='published')
    return render(request, 'author_profile.html', {
        'author_user': author_user,
        'posts': published_posts
    })