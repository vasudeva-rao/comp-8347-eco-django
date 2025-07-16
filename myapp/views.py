from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Tip, UserUpload
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.utils import timezone
from django.views import View
from .forms import CustomUserRegistrationForm
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

class TipListView(ListView):
    model = Tip
    template_name = 'tips_list.html'
    context_object_name = 'tips'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date_added')
        search = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(description__icontains=search)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class VisitHistoryView(View):
    def get(self, request):
        today = timezone.now().date().isoformat()
        visit_count = request.session.get('visit_count', {})
        count = visit_count.get(today, 0) + 1
        visit_count[today] = count
        request.session['visit_count'] = visit_count
        last_5_tips = request.session.get('last_5_tips', [])
        return render(request, 'history.html', {
            'visit_count_today': count,
            'last_5_tips': last_5_tips
        })

class TipDetailView(DetailView):
    model = Tip
    template_name = 'tip_detail.html'
    context_object_name = 'tip'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        tip_id = self.object.pk
        last_5_tips = request.session.get('last_5_tips', [])
        if tip_id in last_5_tips:
            last_5_tips.remove(tip_id)
        last_5_tips.insert(0, tip_id)
        request.session['last_5_tips'] = last_5_tips[:5]
        return response

class TipCreateView(UserPassesTestMixin, CreateView):
    model = Tip
    fields = ['title', 'description', 'category', 'file']
    template_name = 'tip_form.html'
    success_url = reverse_lazy('tips-list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class TipUpdateView(UpdateView):
    model = Tip
    fields = ['title', 'description', 'category', 'file']
    template_name = 'tip_form.html'
    success_url = reverse_lazy('tips-list')

@method_decorator(staff_member_required, name='dispatch')
class TipDeleteView(DeleteView):
    model = Tip
    template_name = 'tip_confirm_delete.html'
    success_url = reverse_lazy('tips-list')

class UserUploadCreateView(LoginRequiredMixin, CreateView):
    model = UserUpload
    fields = ['title', 'file']
    template_name = 'upload_form.html'
    success_url = reverse_lazy('tips-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class HomeView(View):
    def get(self, request):
        tips = Tip.objects.order_by('-date_added')
        return render(request, 'home.html', {'tips': tips})

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

class TeamView(View):
    def get(self, request):
        return render(request, 'team.html')

class UploadGalleryView(View):
    def get(self, request):
        uploads = UserUpload.objects.all().order_by('-upload_date')
        return render(request, 'upload_gallery.html', {'uploads': uploads})

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def bookmark_tip(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    bookmarks = request.session.get('bookmarks', [])
    if pk not in bookmarks:
        bookmarks.append(pk)
        request.session['bookmarks'] = bookmarks
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unbookmark_tip(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    bookmarks = request.session.get('bookmarks', [])
    if pk in bookmarks:
        bookmarks.remove(pk)
        request.session['bookmarks'] = bookmarks
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
