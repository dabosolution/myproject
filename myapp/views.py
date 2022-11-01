from django.views import generic
from .models import Post
from django.db.models import Q
from django.shortcuts import render , redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User, auth 



class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
      model = Post
      template_name = 'post_detail.html'


#this is for the searching functionnality 

def serach(request):
        if 'q' in request.GET:
            q = request.GET['q']
            multiple_q=Q(Q(title__icontains=q))
            posts=Post.objects.filter(multiple_q)
            return render(request,'search.html', {'posts':posts})
        else:
            posts=Post.objects.all()
        return render(request,'index.html',{'posts':posts})


def contact(request):
        if request.method== 'POST':
            try:
                name=request.POST.get('name')
                email=request.POST.get('email')
                phone=request.POST.get('phone')
                message=request.POST.get('message')

                form_data={
                    'name':name,
                    'email':email,
                    'phone':phone,
                    'message':message,
                }
                message=''' 
                From:\n\t\t{}\n
                Message:\n\t\t{}\n
                Email:\n\t\t{}\n
                Phone:\n\t\t{}\n
                '''.format(form_data['name'], form_data['message'], form_data['email'], form_data['phone'])
                send_mail('You got a mail', message , '' , ['daboyakouba22@gmail.com']) #this will be your email address
                messages.success(request,'Message sent successfuly')
            except Exception as e:
                print(e)
                messages.error(request,'Message not Sent Please Try again')
               
        return render(request,'contact.html', {})


def about(request):
    return render(request,'about.html')

def news(request):
    blog= Post.objects.all()
    context={
        'blog':blog
    }   
    return render(request,'news.html', context )

# login system here

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.info(request, 'Username is already taken')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.info(request, 'Email is already taken')

                return redirect("register")
                
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email, first_name=first_name, last_name=last_name)
                user.save()
            return redirect('login')

        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect('register')
    else:
        return render(request,'registration.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')



    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')
