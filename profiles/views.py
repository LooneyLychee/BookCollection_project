from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile, Follow
from .forms import ProfileModelForm
import base64
import requests
from django.core.paginator import Paginator


def upload_file(image):
    response = requests.post("https://api.imgbb.com/1/upload",
                             data={'key': 'c46bc9a4a26941d4b62716eb03df3df8',
                                   'image': image,
                                   'expiration': 60
                                   })
    try:
        response.raise_for_status()
        geodata = response.json()
        return geodata['data']['thumb']['url']
    except requests.exceptions.HTTPError:
        errors = {}
        errors.setdefault('picture', []).append("Bad picture")
        return errors


def follows(request, profile, user_profile):
    if request.method == 'POST':
        follow = Follow.objects.filter(follower=user_profile, followee=profile)
        if follow:
            follow.delete()
        else:
            Follow.objects.create(follower=user_profile, followee=profile)


def my_profile(request, profile):
    form = ProfileModelForm(request.POST or None,
                            request.FILES or None,
                            instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            if 'image' in request.FILES:
                image = base64.b64encode(request.FILES['image'].read())
                form.fields['avatar'].initial = upload_file(image)
                profile.avatar = form.fields['avatar'].initial
                profile.save()
            elif 'submit-default' in request.POST:
                profile.avatar = 'https://i.ibb.co/tKtFPgr/blank-profile-picture-g9a1ddb035-640.png'

            form.save()
    return form


def profile_view(request, profile_id):
    user_profile = None
    profile = Profile.objects.get(id=profile_id)
    profile_owner = False

    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)

    form = None
    if user_profile and profile == user_profile:
        form = my_profile(request, profile)
        profile_owner = True
    elif user_profile:
        follows(request, profile, user_profile)
        profile_owner = False

    context = {
        'form': form,
        'profile': profile,
        'profile_owner': profile_owner,
        'is_followers': Follow.objects.filter(follower=user_profile, followee=profile),
    }

    return render(request, 'profiles/profile.html', context)


def profiles_list_view(request):
    try:
        search_filter = request.GET['search']
    except:
        search_filter = ''
    print(request.GET)
    profiles = Profile.objects.all()
    profiles = profiles.filter(user__username__contains=search_filter) | \
               profiles.filter(first_name__contains=search_filter) | \
               profiles.filter(last_name__contains=search_filter)

    paginator = Paginator(profiles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'profiles/profiles_list.html', context)

