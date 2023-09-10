from django.contrib import admin
from .models import *

@admin.register(Profile) 
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
@admin.register(Client) 
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "contact")

@admin.register(Advert) 
class AdvertAdmin(admin.ModelAdmin):
    list_display =('client','budget','views')
@admin.register(AdvertVideo) 
class AdvertVideoAdmin(admin.ModelAdmin):
    list_display =('client','budget','views')
@admin.register(SocialMedia) 
class SocialMediaAdmin(admin.ModelAdmin):
    list_display =('social',)
@admin.register(JobFeedback) 
class JobFeedbackAdmin(admin.ModelAdmin):
    list_display =('influencer','views','income',)

@admin.register(Help) 
class HelpAdmin(admin.ModelAdmin):
    list_display = ('user','solved','time','description',)

@admin.register(SubmissionReview) 
class SubmissionReviewAdmin(admin.ModelAdmin):
    list_display =('submission','confirmed')

@admin.register(AccountApproval) 
class AccountApprovalAdmin(admin.ModelAdmin):
    list_display =('account','ig_username','views')

@admin.register(Withdrawal) 
class WithdrawalAdmin(admin.ModelAdmin):
    list_display =('user','amount','status')


# ,Advert,SocialMedia,JobFeedback,SubmissionReview,AccountApproval, Withdrawal)   