from django.db import models
from django.contrib.auth.models import User


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_content = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.reply_content

    class Meta:
        verbose_name_plural = "Replies"

    class Meta:
        ordering = ['-date']

    @property
    def get_related_post(self):
        if self.comment_set.first():
            return self.comment_set.first()
        return None

    @property
    def get_related_comment(self):
        if self.comment_set.first():
            return self.comment_set.first().first()
        return None


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)
    approved = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-date']

    @property
    def num_replies(self):
        return self.replies.count()

    @property
    def get_last_reply(self):
        if self.replies.latest("date"):
            return self.replies.latest("date")
        return None

    # @property
    # def get_related_mix(self):
    #     if self.mix_set.first():
    #         return self.mix_set.first().first()
    #     return None

    @property
    def get_replies(self):
        if self.replies.exists():
            return self.replies.order_by("-date")
        return None
