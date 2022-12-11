from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile
from .forms import ProfileModelForm


def my_profile_view(request):
    print(request.user)
    obj = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None,
                            request.FILES or None,
                            instance=obj)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            valid = True

    context = {
        'profile': obj,
        'form': form,
    }

    return render(request, 'profiles/my_profile.html', context)
