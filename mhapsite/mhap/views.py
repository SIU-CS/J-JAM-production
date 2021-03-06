'''
This contains all the logic for how views are handled.
It bridges our Models and Templates.


'''


from django.contrib import messages, auth
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from axes.utils import reset
from django.contrib.sites.shortcuts import get_current_site
from .forms import SignUpForm
from .tokens import activation_token
from .forms import PostForm, AxesCaptchaForm, ProfileForm, UserForm, PasswordForm, ChatForm
from .models import Post, Profile,Quote,ChatMessages

from .bot_helper import Bot
import requests,json

import datetime


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.timezone import utc

# Create your views here.

@login_required
def post_list(request):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    print type(user_prof)
    print type(current_user)
    queryset = Post.objects.user_list(user=user_prof)
    print queryset
    context = {
        "object_list": queryset,
        "title": "Your Blog"
    }
    return render(request, "post_list.html", context)
@login_required
def post_detail(request, slug=None):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    instance = get_object_or_404(Post, slug=slug)
    print "sentiment: " + str(instance.sentiment)
    print "seems depressed: " + str(instance.seems_depressed)
    print "seems suicidal: " + str(instance.seems_suicidal)
    print "secret: " + str(instance.secret)
    print "current user: " + str(user_prof)
    print "blog user: " + str(instance.user_id)
    if instance.secret and (instance.user_id != user_prof):
        raise Http404
    print instance 
    print request.user
    
    # Only show notifications for fresh posts
    current_time = datetime.datetime.utcnow().replace(tzinfo=utc)
    difference = current_time - instance.updated
    if difference.seconds <= 2 * 60:
        if instance.seems_suicidal:
            # I hope this link doesn't rot!
            messages.info(request, mark_safe("<a href='https://suicidepreventionlifeline.org/talk-to-someone-now/'>Suicide is not the answer.</a> Please call 1-800-273-8255 right away."))
        elif instance.seems_depressed:
            messages.info(request, mark_safe("Would you like some <a href='https://www.adaa.org/living-with-anxiety/ask-and-learn/resources'>depression resources</a>?"))
        elif instance.sentiment < 0.3:
            messages.info(request, mark_safe("I\'m sorry you're having a bad day. Would you like some <a href='https://www.adaa.org/tips-manage-anxiety-and-stress'>tips for managing anxiety and stress</a>?"))
        else:
            messages.info(request, "Thank you for posting!")
   # print instance.user_id
    context = {
        "instance": instance,
    }
    return render(request, "post_detail.html", context)
@login_required
def post_create(request):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    form = PostForm(request.POST or None)
    print request.user,"REQUEST"

    if form.is_valid():
        instance = form.save(commit=False)
        print request.user.is_authenticated()
        print "IN VALID"
        #instance.refresh_from_db()
        print Profile.objects.get(user=request.user) , "PROFILE"
        instance.user_id = Profile.objects.get(user=request.user)
        print Profile.objects.get(user=request.user)
        #instance.user = request.user
        print instance.user_id,"USER INSTANCE"
        instance.save()
        print instance.refresh_from_db()
        messages.success(request, "Successfully Created")
        print "succesffuly created"
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

@login_required
def settings(request):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    print user_prof,type(user_prof)
    print current_user,type(current_user)
    instance = get_object_or_404(User, username=current_user)
    instance2 = get_object_or_404(Profile,user=current_user)
    print instance

    form = UserForm(request.POST or None, instance=instance)
    form2 = ProfileForm(request.POST or None, instance=instance2)
    print form2

    form3 = PasswordForm(user=request.user,data=request.POST or None)
    #print "form3," ,form3
    context = {
        'form':form,
        'form2':form2,
        'form3':form3
    }
    #print request.POST
    if form3.is_valid() and form2.is_valid() and form.is_valid():
        print "all forms are valid"
        u_instance=form.save(commit=False)
        
        #messages.success(request, "Saved", extra_tags='html_safe')
        p_instance=form2.save(commit=False)
        u_instance.save()
        p_instance.save()
        print type(form), u_instance.username
        print type(form2), p_instance.birth_date
        print type(form3)
        messages.success(request, "Saved", extra_tags='html_safe')
    return render(request,'settings.html',context)

@login_required
def post_update(request, slug=None):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    instance = get_object_or_404(Post, slug=slug)
    if instance.user_id != user_prof:
        raise Http404
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)

@login_required
def post_delete(request, slug=None):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    instance = get_object_or_404(Post, slug=slug)
    if instance.user_id != user_prof:
        raise Http404
    destination = instance.get_list_url()
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect(destination)

@login_required
def index(request):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    
    queryset = Post.objects.filter(user_id=user_prof)
  
    # Generate mental health visual representation (happy graph)
    data = []
    data_slugs = []
    # Start x-axis at time of your very first post
    if queryset:
        for post in reversed(queryset):
            data.append([post.title.encode('utf-8'), post.sentiment])
            data_slugs.append([post.slug.encode('utf-8')]);
    else:
        # default graph for no-posts users
        data.append(["You have no posts!", 0.5])
  
    instance = queryset.first()

    # if the user has a latest post, display a message if it is older than a day
    if instance:
        # this makes sure the dates are in the same format:
        current_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        difference = current_time - instance.updated
        if difference.days >= 1:
            messages.info(request, "It looks like you haven't posted in awhile, how have you been?")



    quote=None
    try:
        second_quote = Quote.objects.get(id=2)
        quote=second_quote
    except Exception as e:
        print e
    
    context = {
        "data": data,
        "data_slugs": data_slugs,
        "user_prof": user_prof,
        "instance": instance,
        #first variable is what is referenced in html
        #second variable is in code
        "quote_text":second_quote.quote,
        "quote_author":second_quote.author
    }
    return render(request,'index.html', context)

#https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html#sign-up-with-profile-model
def signup(request):
    if request.method == 'POST':
        form  = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.refresh_from_db()
            user.is_active = False
            birth = form.cleaned_data.get('birth_date')
            print birth, "BIRTHDATE"
            user.birth_date = form.cleaned_data.get('birth_date')
            print user.birth_date, "USER BIRTHDATE"
            print user.save()
            #print user.refresh_from_db()
            print user.profile
            print user.birth_date, "USER BIRTHDATE2"
            print user.profile,"PROFILE FAM"
            user.profile.birth_date = birth
            print user.profile.birth_date
            user.profile.save()
            this_site = get_current_site(request)
            subject = "Activate Mhap account"
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain':this_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': activation_token.make_token(user),
            })
            user.email_user(subject,message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        print"CHANGING ACTIVE AND EMAIL CONFIRMED TO TRUE"
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect(reverse("mhap:index"))
        #return redirect('index')
    else:
        return render(request, 'account_activation_invalid.html')

def locked_out(request):
    if request.POST:
        form = AxesCaptchaForm(request.POST)
        if form.is_valid():
            #ip = get_ip_address_from_request(request)
            reset()
            return HttpResponseRedirect('/login')
    else:
        form = AxesCaptchaForm()

    return render(request, 'locked_out.html', dict(form=form))

#https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse("mhap:index"))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', dict(form=form))

@login_required
def bot_page(request):
    #http://stackoverflow.com/questions/40829456/render-form-data-to-the-same-page
    #http://tst07.pythonanywhere.com/post/3/
    info = None
    form = ChatForm(request.POST or None)
    data = ChatMessages.objects.filter(user_id=Profile.objects.get(user=request.user)).order_by('-id')[:10]
    data_reverse = reversed(data)
    context = {
        "form" : form,
        "help_response_one" : Bot.help_response[0],
        "help_response_two" : Bot.help_response[1],
        "data" : data_reverse
    }

    #IF user is posted data
    if form.is_valid():
        print form.cleaned_data
        info = form.cleaned_data['chat']
        
        
        user_prof = Profile.objects.get(user=request.user)
        new_message = ChatMessages.objects.create(message=info, user_id=user_prof,is_user=True)
        message = Bot.process_message(str(info))
        message_type = ChatMessages.DEFAULT
        if type(message) is tuple:
            quote_text = message[0]
            quote_author = message[1]
            print quote_text, quote_author
            message = quote_text + " -" +  quote_author
        elif type(message) is list:
            first_resource = message[0]
            second_resource = message[1]
            print first_resource, second_resource
            message = first_resource + " " + second_resource
            message_type = ChatMessages.RESOURCE

        bot_message = ChatMessages.objects.create(message=message, message_type=message_type, user_id=user_prof,is_user=False) 
        print new_message,"NEW MESSGE"
        print bot_message,"BOT MESSAGE"

        data = ChatMessages.objects.filter(user_id=Profile.objects.get(user=request.user)).order_by('-id')[:10]
        data_reverse = reversed(data)
        context = {
            "form" : form,
            "help_response_one" : Bot.help_response[0],
            "help_response_two" : Bot.help_response[1],
            "data" : data_reverse
        }
        #print context
        
    return render(request, 'bot.html', context)

