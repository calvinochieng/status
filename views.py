from django.contrib.auth import login, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import response
from django.http.response import HttpResponseRedirect, JsonResponse
from .models import AccountApproval, Advert, Interest, JobFeedback, Profile, SocialMedia, Withdrawal,Help,Bonus
from django.db.models import Sum
from .form import ProfileForm, JobFeedbackForm,HelpForm, AccountApprovalForm
from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from datetime import date, datetime

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/status/home/')
    return render(request, 'status/lander.html')
def about(request):
    return render(request, 'status/about.html')

def howto(request):
    return render(request, 'status/howto.html')

def help(request):
    if request.user.is_authenticated:        
        form  = HelpForm()
        if request.method == 'POST':
            if not Help.objects.filter(user = request.user, solved = False).exists():
                form  = HelpForm(request.POST)
                if form.is_valid():
                    description = form.cleaned_data.get('description')
                    help = Help(user = request.user, description = description, )
                    help.save()
                    messages.success(request,"Thank you, we'll get back to you as soon as possible")
                    return HttpResponseRedirect("/status/home/")
                else:
                    messages.warning(request,'Please describe your help again there seem to be a problem')             
            else:
                messages.warning(request,"Sorry, you have a pending issue(s) kindly wait for it to be solved before submitting another, or reach us on our Instagram page @awwzappstatus")
                return HttpResponseRedirect("/status/home/")
        else:
            form = HelpForm()            
    else:
        messages.error(request,'You must be logged in to ask for any help. But you can still contact us on our Instagram page @awwzappstatus', extra_tags='danger ')
    return render(request, 'status/help.html', locals())

@login_required(login_url='/status/login') 
def status(request):
    has_profile  = None
    user = request.user
    active_jobs= Advert.objects.filter(active=True)
    # jobs
    jobfeedback = JobFeedback.objects.filter(influencer=request.user,
                                    withdrawn = False, veryfied =  True)
    if  user.profile.full_name and user.profile.whatsapp:
        has_profile = True
    try:
        verified = AccountApproval.objects.filter(
                        account = request.user, time__isnull=False
                        ).latest('time')
        approved = verified.approved
    except:
        verified = None                           
    try:                            
        jobs = jobfeedback.count()  
    except:
        jobs =  0
    # views
    try:
        views = jobfeedback.aggregate(Sum('submitted_views'))['views__sum']
    except:
        views = 0
    # income
    try:
        income = jobfeedback.aggregate(Sum('income'))['income__sum'] 
    except:
        income = 0
    return render(request,'status/profile.html', locals())

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.warning(request,f'The "{username}" is taken try another one or add underscore ie {username}_ or {username}_001')            
            return render(request, 'status/signup.html')
        elif form.is_valid():
            new_user = form.save()
            new_user.refresh_from_db()
            new_user.save()
            new_user = authenticate(username=form.cleaned_data.get('username'), 
                                    password=form.cleaned_data.get('password1'))
            login(request, new_user)
            messages.success(request,'Account Creation Success! Wellcome...')
            return redirect('/status/home/')
        else:
            messages.error(request,'Error: Try using strong password and nunique one_word username example add underscore john_ or john_doe', extra_tags='danger ')
    else:
        form = UserCreationForm(request.POST)
    return render(request, 'status/signup.html')

@login_required(login_url='/status/login') 
def edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES or None, instance=request.user.profile) 
        birth_date = request.POST.get('birth_date')
        whatsapp = request.POST.get('whatsapp')
        email = request.POST.get('email')
        # birthday validation only 16 years and above
        birthday = datetime.strptime(birth_date, '%Y-%m-%d')
        age_in_days = (date.today()-birthday.date()).days
        age = int(age_in_days)//365.2425
        if age < 16:
            messages.warning(request,f'You must be atleast 16 year, you provided {age}. Come back when you\'re of age')
            return redirect("/status/home/")
        elif Profile.objects.filter(whatsapp=whatsapp).exists():
            messages.warning(request,f'The WhatsApp "{whatsapp}" number provided is already taken, please provide another one')
            return render(request, 'status/editprofile.html',locals())
        elif Profile.objects.filter(email=email).exists():
            messages.warning(request,f'The "{email}" is taken, please provide another one')
            return render(request, 'status/editprofile.html',locals())
        elif form.is_valid():
            form.save()
            messages.success(request,'Profile update was successfull. Now you can start doing the jobs below and earn')
            return redirect("/status/home/")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'status/editprofile.html',locals())
@login_required(login_url='/status/login')
def updateprofile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES or None, instance=request.user.profile) 
        birth_date = request.POST.get('birth_date')
        whatsapp = request.POST.get('whatsapp')
        email = request.POST.get('email')
        user = request.user
        # birthday validation only 16 years and above
        birthday = datetime.strptime(birth_date, '%Y-%m-%d')
        age_in_days = (date.today()-birthday.date()).days
        age = int(age_in_days)//365.2425
        if age < 16:
            messages.warning(request,f'You must be atleast 16 year, you provided {age}. Come back when you\'re of age')
            return redirect("/status/home/")

        elif Profile.objects.exclude(user=user).filter(whatsapp=whatsapp).exists():
            messages.warning(request,f'The WhatsApp "{whatsapp}" number provided is already taken, please provide another one')
            return render(request, 'status/editprofile.html',locals())
        elif Profile.objects.exclude(user=user).filter(email=email).exists():
            messages.warning(request,f'The "{email}" is taken, please provide another one')
            return render(request, 'status/editprofile.html',locals())
        if form.is_valid():
                form.save()
                messages.success(request,'Profile update was successfull.')
                return redirect("/status/home/")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'status/editprofile.html',locals())
@login_required(login_url='/status/login') 
def verifyaccount(request):
    try:
        verified = AccountApproval.objects.filter(account = request.user)
    except:
        verified = False | None
    form = AccountApprovalForm()
    if request.method == 'POST':
        form = AccountApprovalForm(request.POST,request.FILES )
        if form.is_valid():
            account = request.user
            ig_username = form.cleaned_data.get('ig_username')
            screenshot = form.cleaned_data.get('screenshot')
            views = form.cleaned_data.get('views')
            approval = AccountApproval(
                account = account,
                ig_username  = ig_username,
                screenshot = screenshot,
                views = views
            )
            approval.save()
            messages.success(request, "Thank you, your account will be virified soon, wait a bit as we work on it")
            return redirect(status)
        else:
            messages.warning(request, "Some of the fields were not correct, please check again")
            return redirect(status)

    return render(request, 'status/approval.html',locals())
@login_required(login_url='/status/login') 
def job(request, uuid):
    required_views,submissions,remaining_views = 0,0,0
    influencer = request.user
    job = get_object_or_404(Advert, uuid = uuid)
    cost_per_view = job.get_cost_per_view
    platform = SocialMedia.objects.get(pk=2) 
    done = job.jobfeedback_set.filter(influencer = influencer)
    try:
        interest = Interest.objects.filter(viewer = request.user, job = job).latest('date')
    except:
        interest = None
    if interest:
        clicks = interest.clicks +1
        interest = Interest.objects.filter(viewer = request.user, job = job)
        interest.update(clicks = clicks)
    else:
        interest = Interest(viewer = request.user,job = job, clicks = 1, downloads = 0)
        interest.save()
    try:
        account_approval = AccountApproval.objects.filter(
                        account = request.user, time__isnull=False
                        ).latest('time')
        approved_views = account_approval.views
    except:
        account_approval = None

    def approved_views_submit(screenshot,submitted_views,views):
        income_views = float(views)
        income = cost_per_view * income_views               
        job_feedback = JobFeedback(
            influencer = influencer,
            job = job,
            platform = platform,
            screenshot = screenshot,
            submitted_views = submitted_views,
            views = income_views,
            income = income,
            )
        return job_feedback.save()
    def bonus_views_submit(bonus_views):        
        bonus = Bonus(
            influencer = influencer,
            job = job,
            views = bonus_views,
            )
        return bonus.save()

    if account_approval:
        if account_approval.approved:
            if done:
                messages.warning(request, 'You have already submitted that job please try another one, thank you')
                return redirect(status)
            else:
                required_views = job.views

                submissions = job.jobfeedback_set.all().aggregate(Sum('views'))['views__sum'] 
                try:
                    remaining_views = required_views - submissions 
                except:
                    remaining_views = required_views
                form = JobFeedbackForm()
                if request.method == 'POST':
                    form = JobFeedbackForm(request.POST,request.FILES )
                    if form.is_valid():
                        submitted_views = form.cleaned_data.get('views')
                        submitted_views = submitted_views
                        screenshot = form.cleaned_data.get('screenshot')
                        if remaining_views==0:
                            views = 0
                            bonus_views = submitted_views
                            approved_views_submit(screenshot,submitted_views,views)
                            bonus_views_submit(bonus_views)
                            messages.success(request, 'LATE!! submission but the job was submitted successfully, PENDING REVIEW AND CONFIRMQATION')
                            return redirect(status)
                        elif submitted_views <= approved_views  and  approved_views <= remaining_views: 
                            views = submitted_views
                            approved_views_submit(screenshot,submitted_views,views)
                            messages.success(request, 'Job submitted successfully, PENDING REVIEW AND CONFIRMQATION')
                            return redirect(status)
                        elif submitted_views>approved_views and approved_views <=remaining_views:
                            views = approved_views
                            bonus_views = submitted_views - views
                            approved_views_submit(screenshot,submitted_views,views)
                            bonus_views_submit(bonus_views)
                            messages.success(request, 'Job submitted successfully, PENDING REVIEW AND CONFIRMQATION')
                            return redirect(status)
                        elif submitted_views>approved_views and approved_views > remaining_views:
                            views = remaining_views
                            bonus_views = submitted_views - views
                            approved_views_submit(screenshot,submitted_views,views)
                            bonus_views_submit(bonus_views)
                            messages.success(request, 'Job submitted successfully, PENDING REVIEW AND CONFIRMQATION')
                            return redirect(status)
            
        else:
            messages.warning(request, 'Sorry you can\'t do this job.Your account is pending approval, HOLD ON A BIT WE\'RE WORKING ON IT')
            return redirect(status)
    elif account_approval == None:
        messages.warning(request,"Sorry your account is not yet VERIFIED, GET YOUR ACCOUNT APPROVED THEN TRY AGAIN")
        return redirect(status)
    else:
        return render(request, 'status/job.html',locals())
    return render(request, 'status/job.html',locals())
@login_required(login_url= '/status/login')
def download(request,uuid):    
    job = get_object_or_404(Advert, uuid = uuid)
    interest = Interest.objects.filter(viewer = request.user, job = job)
    if request.method =='POST':
        if interest:
            downloads = interest.downloads +1
            interest.update(downloads = downloads)
            return JsonResponse({'ok':"Okay"})
        else:
            pass        
    return JsonResponse({'not_okay':"nooo just dont visit this"})


@login_required(login_url='/status/login') 
def withdraw(request):
    threshold = 100.00
    # jobs
    jobfeedback = JobFeedback.objects.filter(influencer = request.user, withdrawn = False, veryfied = True)
    # income
    try:
        income = jobfeedback.aggregate(Sum('income'))['income__sum'] 
    except:
        income = 0
    
    jobs = jobfeedback.count()  
    # views
    views = jobfeedback.aggregate(Sum('views'))['views__sum']
    today = date.today()
    withdrawals = Withdrawal.objects.filter(user = request.user)        
    if request.method == 'POST':
        if income is not None and income > threshold:
            data = {
                "details":{"income": float(income),
                    "views": views,
                    "jobs" : jobs,
                    "job_ids" : list(jobfeedback.values_list('id', flat=True))}
            }
            form = Withdrawal.objects.create(
                user = request.user,
                amount = income,
                details = data,
            )
            jobfeedback.update(withdrawn = True)
            messages.success(request,f"You have successfully withdrawn KESH {income} which will be sent to {request.user.profile.whatsapp} M.pesa, kindly wait for processing.")
            return HttpResponseRedirect('/status/withdraw/')
        else:
            messages.warning(request,"Your earnings is below threshold, it must be KESH 100.00 or more for you to withdraw")
            return HttpResponseRedirect('/status/withdraw/')
    return render(request,'status/withdraw.html', locals())

@staff_member_required(login_url='/status/login')
def dashboard(request):
    if request.user.is_superuser:
        return render(request,'status/dashboard.html')
