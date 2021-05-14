
from django.db import models
from apps.app1.models import User



# Create your models here.
class MessageManager(models.Manager):
    def validator(self, postData):
        errors ={}
        if len(postData['messagesHTML']) < 2:
            errors['messagesHTML'] = "El mensaje debe ser mayor a 1 caracter"
        return errors 



class Message(models.Model):
    message = models.TextField()
    # Uno (user) a muchos (Message)
    users = models.ForeignKey(User, related_name="user_messages", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()


class CommentManager(models.Manager):
    def validator(self, postData):
        errors ={}
        if len(postData['commentHTML']) < 2:
            errors['commentHTML'] = "El comentario debe ser mayor a 1 caracter"
        return errors 

class Comment(models.Model):
    comment = models.TextField()
    # Uno (User) a muchos (Comment)
    users = models.ForeignKey(User, related_name="coments_of_user", on_delete = models.CASCADE)
    # Uno (Message) a muchos (Comment)
    messages = models.ForeignKey(Message, related_name="comments_of_messages", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
