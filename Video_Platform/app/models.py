import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.utils import timezone

def time_since(uploaded_at):
    now = timezone.now()  # timezone aware current time
    diff = now - uploaded_at  # uploaded_at should also be timezone aware

    seconds = diff.total_seconds()
    if seconds < 0:
        seconds = abs(seconds)  # just in case

    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24

    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif minutes < 60:
        return f"{int(minutes)} minutes ago"
    elif hours < 24:
        return f"{int(hours)} hours ago"
    else:
        return f"{int(days)} days ago"


# Create your models here.
class Profile(models.Model):    
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.CharField(max_length=10)
    photo=models.ImageField(upload_to="upload_profile/")
    banner_image=models.ImageField(upload_to="upload_profile/")
    created_at = models.DateTimeField(default=datetime.now())     
    subscriptions=models.ManyToManyField('self',symmetrical=False,related_name='subscribers',blank=True)

    def __str__(self):
        return self.user.username

class Videos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos') 
    caption=models.CharField(max_length=100,blank=True)
    title=models.CharField(max_length=100)
    comment=models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(default=datetime.now()) 
    video=models.FileField(upload_to="video/%y")    
    tumbnail=models.ImageField(upload_to="upload_profile/")
    views = models.PositiveIntegerField(default=0)
    viewers = models.ManyToManyField(User, related_name='viewed_videos', blank=True)


    def time_since_uploaded(self):
        return time_since(self.uploaded_at)


class Comment(models.Model):
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} on {self.video.title}"


class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name='likes_dislikes')
    value = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])

    class Meta:
        unique_together = ('user', 'video')  # Prevent multiple likes/dislikes from same user
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') 
    caption = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(default=datetime.now) 
    image = models.ImageField(upload_to="upload_profile/")

    def __str__(self):
        return f"{self.user.username} - {self.caption}" 


class PostLikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes_dislikes')
    value = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} - {self.value} - {self.post.id}"
    




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.user.username}"
    
class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_history')
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-watched_at']  # newest first