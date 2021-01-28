from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry, Comment, Like
from .forms import TopicForm, EntryForm, CommentForm
from django.http import Http404


def index(request):
    """
    The Home page for learning Log
    """
    topic = Topic.objects.all()
    context = {
        'topic': topic,
    }
    return render(request, 'blog_app/index.html', context)


@login_required
def topics(request):
    """
    Show All Topics
    """
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'blog_app/topics.html', context)


@login_required
def topic(request, topic_id):
    """
    Show a single topic and all its entries
    """
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'blog_app/topic.html', context)


@login_required
def new_topic(request):
    """
    Add a New Topic
    """
    if request.method != 'POST':

        form = TopicForm()
    else:

        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('blog_app:topics')
    context = {'form': form}
    return render(request, 'blog_app/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """
    Add a New Topic
    """
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':

        form = EntryForm()
    else:

        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('blog_app:topic', topic_id=topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'blog_app/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """
    Add a New Topic
    """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':

        form = EntryForm(instance=entry)
    else:

        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_app:topic', topic_id=topic.id)
    context = {'topic': topic, 'form': form, 'entry': entry}
    return render(request, 'blog_app/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):
    """
    Add a New Topic
    """
    entry = Entry.objects.get(id=entry_id)
    entry.delete()
    return redirect('blog_app:topics')


@login_required
def comment_entry(request, entry_id):
    post = Entry.objects.get(id=entry_id)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "blog_app/comments.html", context)
