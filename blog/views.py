from django.shortcuts import render
from .models import Post, Comment
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post= get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull = True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_delete(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')

def signup(request):
    if request.method == "POST":
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
        return redirect('post_list')
    else:
        signup_form = UserCreationForm()
    return render(request, 'registration/signup.html', {'signup_form': signup_form})

@login_required
def add_comment(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post

            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})


@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request,pk,cpk):
    comment = get_object_or_404(Comment, pk=cpk)

    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_edit(request,pk,cpk):
    post = get_object_or_404(Post,pk=pk)
    comment = get_object_or_404(Comment,pk=cpk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = 'admin'
            comment.save()
            return redirect('comment_detail', pk=post.pk, cpk=comment.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html',{'form':form})

@login_required
def comment_detail(request,pk,cpk):
    post = get_object_or_404(Post,pk=pk)
    comment = get_object_or_404(Comment, pk=cpk)
    return render(request, 'blog/comment_detail.html',{'post':post, 'comment': comment})
