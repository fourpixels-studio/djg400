from mixes.models import Mix
from .models import Comment, Reply
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def comment_mix(request, pk):
    mix = Mix.objects.get(pk=pk)
    if request.method == 'POST':
        comment_content = request.POST.get("comment")
        if comment_content is not None and comment_content.strip() != "":
            new_comment, created = Comment.objects.get_or_create(user=request.user, comment_content=comment_content)
            new_comment.save()
            mix.comments.add(new_comment.id)
    return redirect("mix_detail", mix.slug)


@login_required
def comment_reply(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == 'POST':
        reply_content = request.POST.get("reply")
        if reply_content is not None and reply_content.strip() != "":
            new_reply, created = Reply.objects.get_or_create(
                user=request.user, reply_content=reply_content)
            new_reply.save()
            comment.replies.add(new_reply.id)
    return redirect("index")
    # return redirect("mix_detail", comment.get_related_mix.slug)
