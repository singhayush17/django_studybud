from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True,default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []




class Topic(models.Model):
    name = models.TextField(max_length=200)

    def __str__(self):
        return self.name    




class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    topic=  models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True) #if set null allow it to be null (null=Trues)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True) #null=True means can be blank
    participants = models.ManyToManyField(User,related_name='participants',blank=True) #cannot use User as User already taken 
    updated = models.DateTimeField(auto_now=True) #when saved take timestamp
    created = models.DateTimeField(auto_now_add=True) #takes timestamp when FIRST SAVED

    class Meta:
        ordering = ['-updated','-created'] #value --> ascending order , -value descending order


    def __str__(self):
        return str(self.name)




class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #IF ROOM deleted all messages deleted
    body=models.TextField()
    updated = models.DateTimeField(auto_now=True) #when saved take timestamp
    created = models.DateTimeField(auto_now_add=True) #takes timestamp when FIRST SAVED
    
    class Meta:
        ordering = ['-updated','-created'] 

    def __str__(self):
        return str(self.body[0:50])
 

