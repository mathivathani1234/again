from django.shortcuts import redirect, render
from django.contrib.auth import login,logout,authenticate
from .form import *
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
@login_required(login_url='login')
# Create your views here.
def home(request):
   if request.method == 'POST':
     print(request.POST)
     questions= QuestionsModel.objects.all()
     score=0
     wrong=0
     correct=0
     total=0
     all_answered=True
     for q in questions:
       total+=1
       user_answer = request.POST.get(f"question_{q.id}") 
       if user_answer:
          if user_answer == q.answer:
              score+=10
              correct+=1
          else:
              wrong+=1
       else:
         all_answered = False
     if not all_answered:
        context = {'questions': questions, 'error': 'Please answer all questions.', 'user_answers': request.POST} 
        return render(request, 'home.html', context)
     percent=score/(total*10)*100
     context={
           'score':score,
           'correct':correct,
           'wrong':wrong,
           'percent':percent,
           'total':total,
     }
     return render(request,'result.html',context)
   else:
        questions= QuestionsModel.objects.all()
        context = {
           'questions':questions
           }
        return render(request,'home.html',context)
def registerPage(request):
     if request.user.is_authenticated:
        return redirect('home')
     else:
        form = createuserform()
        if request.method=='POST':
           form = createuserform(request.POST)
           if form.is_valid():
              user=form.save()
              return redirect('login')
        context={
              'form':form,
              }
        return render(request,'register.html',context)
def loginPage(request):
   if request.user.is_authenticated:
      return redirect('home')
   else:
      if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
           login(request,user)
           return redirect('home')
        else:
           context={'error': 'Invalid username or password'}
           return render(request,'login.html', context)
      context={}
      return render(request,'login.html',context)
def logoutPage(request):
    auth.logout(request)
    return redirect('login')