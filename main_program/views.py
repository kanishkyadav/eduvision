from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import LoginForm, UserSignUpForm
from .models import Post, Category
from .forms import PostForm
from django.views.generic import ListView, CreateView, FormView


class PostView(ListView):
    model = Post
    paginate_by = 1
    # context_object_name = 'post'  # Default: object_list
    template_name = 'main_program/blog.html'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        context = super(PostView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.filter(category__slug=slug)
        context['slug'] = slug
        return context

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs.get('slug')).order_by('id')


class Home(ListView):
    modle = Category
    template_name = 'main_program/home.html'

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if not query:
            return Category.objects.all().order_by('?')[:6]
        else:
            from django.contrib.postgres.search import SearchRank, SearchQuery, SearchVector
            vector = SearchVector("title")
            nQuery = SearchQuery(query)
            result = Post.objects.annotate(rank=SearchRank(vector, nQuery)).filter(rank__gte=0.001).order_by("-rank")
            return result


# @method_decorator(staff_member_required, name='dispatch')
class Programs(CreateView):
    template_name = 'main_program/program.html'
    form_class = PostForm
    success_url = '/program/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = User.objects.get(username=self.request.user)
        kwargs.update({'initial': {'author': user}})
        return kwargs

    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super().form_valid(form)


class SignUpFormView(FormView):
    template_name = 'main_program/register.html'
    form_class = UserSignUpForm
    success_url = '/'

    usersignup = "active"
    status = False

    def get_context_data(self, **kwargs):
        context = super(SignUpFormView, self).get_context_data(**kwargs)
        context.update({'usersignup': self.usersignup})
        return context

    def form_valid(self, form):
        if form.is_valid():
            messages.success(self.request, 'Account Created Successfully !!')
            form.save()
        return super().form_valid(form)


class UserloginForm(LoginView):
    template_name = 'main_program/login.html'
    authentication_form = LoginForm
    login = "active"

    def get_context_data(self, **kwargs):
        context = super(UserloginForm, self).get_context_data(**kwargs)
        context.update({'login': self.login})
        return context

    def form_valid(self, form):
        uname = form.cleaned_data['username']
        upass = form.cleaned_data['password']
        user = authenticate(username=uname, password=upass)
        # checking user
        if user.is_superuser:
            login(self.request, user)
            messages.success(self.request, 'Logged in successfully !!')
            return HttpResponseRedirect('/home/')

        if user.is_staff:
            login(self.request, user)
            messages.success(self.request, 'Logged in successfully !! ')
            return HttpResponseRedirect('/home/')

        if user.is_active:
            login(self.request, user)
            messages.success(self.request, 'Logged in successfully !!')
            return HttpResponseRedirect('/home/')
        else:
            return HttpResponseRedirect('/login/')
        return super().form_valid(form)


def Contact(request):
    from .models import ContactUs
    if request.method == "POST":
        cForm = ContactUs()
        cForm.name = request.POST.get("name")
        cForm.email = request.POST.get("email")
        cForm.comment = request.POST.get("comment")
        cForm.save()
        messages.success(request,"Contact form summited.!!")
        return redirect('/')
    return render(request, 'main_program/contact.html')