from datetime import date
import uuid
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dp = CloudinaryField('pd')
    full_name = models.CharField(max_length=100, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    client = models.BooleanField(null= True, default= False)
    approved = models.BooleanField(null= True, default= False)
    birth_date = models.DateField(null=True,blank=True)
    def __str__(self):
        return self.user.username
    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

class AccountApproval(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ig_username = models.CharField(max_length=200)
    screenshot = CloudinaryField('approval_screenshot',blank=True, null=True)
    views = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    time = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True, )
    class Meta:
        verbose_name = 'AccountApproval'
        verbose_name_plural = 'AccountApprovals'
    def __str__(self):
        return f'{self.account.username}, {self.ig_username}'

class Help(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=False, null=False)
    solved = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Help'
        verbose_name_plural = 'Helps'
    def __str__(self):
        return self.user.username

class Client(models.Model):
    name = models.CharField(max_length=300,blank=False)
    description = models.TextField()
    address = models.CharField(max_length=300)
    contact = models.CharField(max_length=200,blank=False)
    joined = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
    def __str__(self):
        return self.name


class Advert(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    admin  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    file  =  CloudinaryField('advert_image')
    video = CloudinaryField('advert_video',blank=True, null=True)
    remarks = models.TextField()
    budget = models.IntegerField(default=0)
    percentage = models.DecimalField(null=True, max_digits=4, decimal_places=3, default=0)
    platform = models.ForeignKey('SocialMedia', on_delete= models.CASCADE, null = True )
    views = models.IntegerField(default=0, null=True)
    active = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    class Meta:
        ordering = ["-date"]
        verbose_name = 'Advert'
        verbose_name_plural = 'Adverts'
    @property
    def get_cost_per_view(self):
        jv = self.views
        jb = self.budget
        jp = self.percentage
        try:
            if self.percentage or self.percentage == 0:
                return (jb/jv)*float(jp)
            else:
                return (self.budget/self.views)*0.5
        except:
            return 0
    def __str__(self):
        return self.client.name
class AdvertVideo(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    admin  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    video  =  CloudinaryField('advert_video')
    remarks = models.TextField()
    budget = models.IntegerField(default=0)
    percentage = models.DecimalField(null=True, max_digits=4, decimal_places=3, default=0)
    platform = models.ForeignKey('SocialMedia', on_delete= models.CASCADE, null = True )
    views = models.IntegerField(default=0, null=True)
    active = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    class Meta:
        ordering = ["-date"]
        verbose_name = 'AdvertVideo'
        verbose_name_plural = 'AdvertVideos'
    @property
    def get_cost_per_view(self):
        jv = self.views
        jb = self.budget
        jp = self.percentage
        try:
            if self.percentage or self.percentage == 0:
                return (jb/jv)*float(jp)
            else:
                return (self.budget/self.views)*0.5
        except:
            return 0
    def __str__(self):
        return self.client.name

class SocialMedia(models.Model):
    social = models.CharField(max_length=50)
    modified  = models.DateField(auto_now_add= True)
    class Meta:
        verbose_name = 'SocialMedia'
        verbose_name_plural = 'SocialMedias'
    def __str__(self):
        return self.social
        


class JobFeedback(models.Model):
    influencer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Advert, on_delete=models.CASCADE)
    platform = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    screenshot = CloudinaryField('feedback_screenshot')
    submitted_views = models.IntegerField(default=0,blank=False,null= True)
    views = models.IntegerField(default=0,blank=False)
    income = models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)
    withdrawn = models.BooleanField(null=True, default=False)
    veryfied = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add= True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'JobFeedback'
        verbose_name_plural = 'JobFeedbacks'
    def __str__(self):
        return f'{self.influencer.username},{self.id}, {self.views}'
class Interest(models.Model):
    viewer =  models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Advert, on_delete=CASCADE)
    clicks = models.IntegerField(default = 0) 
    downloads = models.IntegerField(default=0, blank= True, null=True)   
    date = models.DateTimeField(auto_now_add= True)
    modified = models.DateTimeField(auto_now=True)
    # TODO: Define fields here

    class Meta:
        """Meta definition for Interest."""

        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'

    def __str__(self):
        """Unicode representation of Interest."""
        pass


class Bonus(models.Model):
    influencer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Advert, on_delete=models.CASCADE)
    views = models.IntegerField(default=0,blank=False)
    withdrawn = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add= True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Bonus'
        verbose_name_plural = 'Bonuses'

    def __str__(self):
        return self.influencer.username


class SubmissionReview(models.Model):
    """Model definition for SubmissionReview."""
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submission = models.ForeignKey('JobFeedback', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'SubmissionReview'
        verbose_name_plural = 'SubmissionReviews'

    def __str__(self):
        return self.reviewer.name

class Withdrawal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.00, max_digits=8, decimal_places=2, blank=True)
    details = models.JSONField()
    cashedout = models.BooleanField(default=False)
    status = models.CharField(max_length=1, default='p',null=True, choices=[
        ('p','Pending'),('w','Withdrawn'),('c','Cancelled')]
        )
    date = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Withdrawal'
        verbose_name_plural = 'Withdrawals'
    def __str__(self):
        return self.user.username
