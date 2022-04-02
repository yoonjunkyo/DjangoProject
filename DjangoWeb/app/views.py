"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
import os
import numpy as np
import pandas as pd
from sklearn import datasets
from django.conf import settings
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from sklearn.ensemble import RandomForestClassifier
import pickle
from app.models import Post

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )



def blog(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

        # 모든 Post를 가져와 postlist에 저장합니다
    postlist = Post.objects.all()
    # blog.html 페이지를 열 때, 모든 Post인 postlist도 같이 가져옵니다 
    return render(
        request, 
        'app/blog.html', 
        {
            'postlist':postlist,
            'title':'Blog',
            'message':'Your blog page.',
            'year':datetime.now().year,
        }
    )

def posting(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    post = Post.objects.get(pk=pk)
    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(
        request, 
        'app/posting.html', 
            {
            'post':post
            }
    )

def new_post(request):
    if request.method == 'POST':
        if request.POST['mainphoto']:
            new_article=Post.objects.create(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                mainphoto=request.POST['mainphoto'],
            )
        else:
            new_article=Post.objects.create(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                mainphoto=request.POST['mainphoto'],
            )
        return redirect('/blog/')
    return render(request, 'app/new_post.html')

def remove_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/blog/')
    return render(request, 'app/remove_post.html', {'Post': post})


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def Train(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/Train.html',
        {
            'title':'Train',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


class IrisTrain(views.APIView): 
    """
    POST
    """
    def post(self, request):
        iris = datasets.load_iris()
        mapping = dict(zip(np.unique(iris.target),iris.target_names))

        X = pd.DataFrame(iris.data, columns=iris.feature_names)
        y = pd.DataFrame(iris.target).replace(mapping)
        model_name = request.data.pop('model_name')

        try:
            clf = RandomForestClassifier(**request.data)
            clf.fit(X,y)

        except Exception as err:
            return Response(str(err),status=status.HTTP_400_BAD_REQUEST)

        path = os.path.join(settings.MODEL_ROOT,model_name)
        with open(path,'wb') as file:
            pickle.dump(clf,file)
        return Response(status=status.HTTP_200_OK)


class IrisPredict(views.APIView):
    """
    POST
    """
    def post(self, request):
        predictions = []
        for entry in request.data:
            model_name = entry.pop('model_name')
            path = os.path.join(settings.MODEL_ROOT,model_name)
            with open(path,'rb') as file:
                model = pickle.load(file)
            try:
                result = model.predict(pd.DataFrame([entry]))
                predictions.append(result[0])

            except Exception as err:
                return Response(str(err),status=status.HTTP_400_BAD_REQUEST)
        return Response(predictions, status=status.HTTP_200_OK)
