from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    print('share')
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            body = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            # Setup the MIME
            message = MIMEMultipart()
            message['From'] = 'test_edge@mail.ru'
            message['To'] = cd['to']
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            session = smtplib.SMTP('smtp.mail.ru', 2525)  # use gmail with port
            session.starttls()  # enable security
            password = os.environ.get("EMAIL_HOST_PASSWORD")
            session.login('test_edge@mail.ru', password)  # login with mail_id and password
            session.send_message(message)
            session.quit()
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
