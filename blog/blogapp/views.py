from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.http import Http404
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm

class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blogapp/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
    Post,
    status=Post.Status.PUBLISHED,
    slug=post,
    publish__year=year,
    publish__month=month,
    publish__day=day)
    return render(request,
        'blogapp/post/detail.html',
        {'post': post})

def post_share(request, post_id):
    # Retrieve post by id
    sent=False
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blogapp/post/share.html', {'post': post,'form': form,'sent':sent})