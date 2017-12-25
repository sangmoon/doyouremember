from .forms import SignUpForm, MemoryForm
from .tokens import account_activation_token
from .models import Memory, Profile

from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.


def home(request):
    form = MemoryForm
    return render(request, 'home.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # user creation...
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your DoYouRemember Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html', {})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


@login_required
def memory(request):
    if request.method == 'POST':
        form = MemoryForm(request.POST)
        if form.is_valid():
            new_memory = Memory(user=request.user,
                                content=form.cleaned_data['content'])
            new_memory.save()
            return HttpResponse("Your Memory is saved")
    else:
        form = MemoryForm()
    return render(request, 'home.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        try:
            received_email = request.POST.get('user-received-email', user.email)
            validate_email(received_email)
        except ValidationError as e:
            print(e)
        else:
            user.profile.received_email = received_email
            user.save()

    else:
        user = request.user
    return render(request, 'profile.html',
                  {'user': user})
