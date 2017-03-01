
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import activation_token
from django.contrib.sites.shortcuts import get_current_site
from .forms import PostForm
from .models import Post,Profile
from django.contrib.auth.models import User
# Create your views here.

# def index(request):
#     return HttpResponse("Hello dawgs. This is mhap.")
@login_required
def post_list(request):
    print request.user
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "title": "List"
    }
    return render(request, "post_list.html", context)
@login_required
def post_detail(request, slug=None):
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
def post_create(request):
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
def post_update(request, slug=None):
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
def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("mhap:list")


# Create your views here.

@login_required
def index(request):
    return render(request,'index.html')

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
        return redirect('index')
    else:
        return render(request, 'account_activation_invalid.html')
