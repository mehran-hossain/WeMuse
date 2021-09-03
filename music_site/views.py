from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from .filters import AudioFilter
from .forms import UserRegisterFrom, UserUpdateForm, AudioUploadForm
from musix.models import Audio, Sample
from django.contrib.auth.models import User


@login_required(redirect_field_name='welcome')
def home(request):
    uploads = Audio.objects.filter(uploader=request.user).all()
    return render(request, 'music_site/home.html', {'uploads': uploads})


def register(request):
    if request.method == "POST":
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterFrom()
    return render(request, "music_site/register.html", {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Profile Updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {'u_form': u_form}
    return render(request, 'music_site/profile.html', context)


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')


def upload_list(request):
    uploads = Audio.objects.all()
    myFilter = AudioFilter(request.GET, queryset=uploads)
    uploads = myFilter.qs
    return render(request, 'music_site/upload_list.html', {'uploads': uploads, 'filter': myFilter})


@login_required
def upload(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploader = User.objects.get(pk=request.user.id)
            obj.save()
            return HttpResponseRedirect(reverse('details',
                                                args=(obj.pk,
                                                      )))
    else:
        form = AudioUploadForm()
    return render(request, 'music_site/upload.html', {'form': form})


@login_required
def addSample(request, pk1, pk2):
    if request.method == 'POST':
        bool = True
        for i in Sample.objects.all():
            if i.main == Audio.objects.get(pk=pk1) and i.sub == Audio.objects.get(pk=pk2):
                bool = False
        if bool:
            b = Sample(main=Audio.objects.get(pk=pk1), sub=Audio.objects.get(pk=pk2))
            b.save()
            obj = Audio.objects.get(pk=pk2)
            obj.sample_count += 1
            obj.save()
    return HttpResponseRedirect(reverse('details',
                                        args=(pk1,
                                              )))


def delete(request, pk):
    if request.method == 'POST':
        audio = Audio.objects.get(pk=pk)
        audio.delete()
        return redirect('home')


class Details(DetailView):
    model = Audio
    template_name = "music_site/details.html"

    def get_context_data(self, **kwargs):
        context = super(Details, self).get_context_data(**kwargs)
        context['filter'] = AudioFilter(self.request.GET, queryset=self.get_queryset())
        # context['first'] = Audio.objects.filter(uploader=self.request.user).first()  # this is a thing
        context['sample'] = Sample.objects.all()
        context['current_obj'] = self.get_object()
        return context


def deleteSample(request, pk, pk1, pk2):
    if request.method == 'POST':
        sample = Sample.objects.get(pk=pk)
        sample.delete()
        obj = Audio.objects.get(pk=pk2)
        obj.sample_count -= 1
        obj.save()
        return HttpResponseRedirect(reverse('details',
                                            args=(pk1,
                                                  )))



