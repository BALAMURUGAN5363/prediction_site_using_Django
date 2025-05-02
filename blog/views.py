from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import logging

posts = [
        {'id':'Diabetees_Prediction','tittle' : 'Diabetees Prediction', 'content' : 'content of Diabetees Prediction'},
        {'id':'Ipl_prediction','tittle' : 'IPL Winning Team Prediction', 'content' : 'content of IPL Prediction'},
        {'id': 'car_price_prediction', 'tittle': 'Car Price Prediction', 'content': 'Predict the price of used cars'},
        {'id':4,'tittle' : 'Weather Prediction', 'content' : 'content of Diabetees Prediction'},
        {'id':5,'tittle' : 'House Price Prediction', 'content' : 'content of Diabetees Prediction'},
        {'id':6,'tittle' : 'Heart Disease Prediction', 'content' : 'content of Diabetees Prediction'},
    ]

def index(request):
    blog_title = 'Prediction Models'
    return render(request,'blog/index.html',{'blog_title':blog_title, 'posts' : posts})

def detail(request, post_id):
    post = next((item for item in posts if item['id'] == post_id), None)
    logger = logging.getLogger('TESTING')
    logger.debug(f'post variable is {post}')
    
    if post_id == 'Diabetees_Prediction':
        return render(request, 'diabetes_predictor/form.html', {'post': post})
    elif post_id == 'Ipl_prediction':
        return render(request, 'ipl_prediction/ipl_form.html', {'post': post})
    elif post_id == 'car_price_prediction':
        return render(request, 'car_price_prediction/form.html', {'post': post})
    
    return render(request, 'blog/detail.html', {'post': post})

def old_url_redirect(request):
    return redirect(reverse('blog:new_url'))

def new_url_view(request):
    return HttpResponse("This is the new url")



# Create your views here.
