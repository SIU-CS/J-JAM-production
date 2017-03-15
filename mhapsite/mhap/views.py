'''
TODO
1. Settings page with username,birthdate change and password change

#https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html

'''


from django.contrib import messages, auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth import login,authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import activation_token
from django.contrib.sites.shortcuts import get_current_site
from .forms import PostForm,AxesCaptchaForm,ProfileForm,UserForm
from .models import Post,Profile
from django.contrib.auth.models import User
from axes.utils import reset


# Create your views here.

@login_required
def post_list(request, username=None):
    current_user = Profile.objects.get(user=request.user).user
    blog_user = get_object_or_404(User, username=username)
    user_prof = get_object_or_404(Profile, user=blog_user)
    print type(user_prof)
    print str(username)
    print str(request.user)
    print "BEFORE IF"
    if(blog_user != current_user): 
        print "IN IF"
        raise Http404
    print "AFTER IF"
    if ((not current_user.is_staff) and (not current_user.is_superuser)) and (blog_user.is_staff or blog_user.is_superuser):
        raise Http404
    queryset = Post.objects.filter(user_id=user_prof)
    print queryset
    context = {
        "object_list": queryset,
        "title": "List"
    }
    return render(request, "post_list.html", context)
@login_required
def post_detail(request, username=None, slug=None):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    blog_user = get_object_or_404(User, username=username)
    if ((not current_user.is_staff) and (not current_user.is_superuser)) and (blog_user.is_staff or blog_user.is_superuser):
        raise Http404
    if current_user != blog_user:
        instance = get_object_or_404(Post, slug=slug, secret=False)
    else:
        instance = get_object_or_404(Post, slug=slug)
    print instance 
    print request.user
   # print instance.user_id
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "post_detail.html", context)
@login_required
def post_create(request, username=None):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    blog_user = get_object_or_404(User, username=username)
    if (current_user != blog_user) and (not current_user.is_staff) and (not current_user.is_superuser):
        raise Http404
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
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

@login_required
def settings(request,username=None):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    print user_prof
    print current_user
    instance = get_object_or_404(User,username=current_user)
    print instance
    #form = ProfileForm(request.POST or None,instance=instance)
    #print form

    form2 = UserForm(request.POST or None, instance=instance)
    print form2
    context = {
        'form':form2,
    }
    if form2.is_valid():
        instance = form2.save(commit=False)
        instance.save()
        messages.success(request, "Saved", extra_tags='html_safe')
        return redirect(reverse("mhap:index", kwargs={"username": request.user}))
    return render(request,'settings.html',context)

@login_required
def post_update(request, username=None, slug=None):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    blog_user = get_object_or_404(User, username=username)
    if (current_user != blog_user) and (not current_user.is_staff) and (not current_user.is_superuser):
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
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
def post_delete(request, username=None, slug=None):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    blog_user = get_object_or_404(User, username=username)
    if (current_user != blog_user) and (not current_user.is_staff) and (not current_user.is_superuser):
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    destination = instance.get_list_url()
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect(destination)

def base(request):
    return redirect(reverse("mhap:index", kwargs={"username": request.user}))


@login_required
def index(request, username=None):
    user_prof = Profile.objects.get(user=request.user)
    current_user = user_prof.user
    blog_user = get_object_or_404(User, username=username)
    if (current_user != blog_user) and (not current_user.is_staff) and (not current_user.is_superuser):
        raise Http404
    context = {
        "user": blog_user
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
        return redirect(reverse("mhap:index", kwargs={"username": user}))
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

    return render(request,'locked_out.html', dict(form=form))