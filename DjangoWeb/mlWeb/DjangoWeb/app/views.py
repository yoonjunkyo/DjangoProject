"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
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

def Predict(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/Predict.html',
        {
            'title':'Predict',
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
