from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as auth_logout
import numpy as np
import joblib
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from . models import UserPredictModel
from .forms import UserPredictDataForm




Model = joblib.load('C:/Users/SPIRO-JAVA NEW/Videos/ITPML37-FINAL/ITPML37-FINAL CODING/Deployment/users/Model.pkl')
def model(request):
    if request.method == 'POST':
        fields =['Air_temperature', 'Process_temperature', 'Rotational_speed', 'Torque', 'Tool_wear']
      
        
        form = UserPredictDataForm(request.POST)
        features = []
        for i in fields:
            info = float(request.POST[i])
            features.append(info)
           
        Final_features = [np.array(features, dtype=int)]
        
        prediction = Model.predict(Final_features)
        actual_output = prediction[0]
        print(actual_output)

        if actual_output == 0:
            actual_output1 = 'Heat Dissipation Failure'
            
        elif actual_output == 1:
            actual_output1 = 'No Failure'
        
        elif actual_output == 2:
            actual_output1 = 'Overstrain Failure'

        elif actual_output == 3:
            actual_output1 = 'Power Failure'

        elif actual_output == 4:
            actual_output1 = 'Random Failures'

        elif actual_output == 5:
            actual_output1 = 'Tool Wear Failure'


      
        print("output",actual_output1)
        if form.is_valid():
            print('Saving data in Form')
            form_instance = form.save()  # Save form data but don't commit to DB yet
            form_instance.save()
        data = UserPredictModel.objects.latest('id')
        data.Label = actual_output1
        data.save()
        return render(request, 'app/result.html', {'form':form, 'prediction_text':actual_output1})
    else:
        print('Else working')
        form = UserPredictDataForm(request.POST)    
    return render(request, 'app/model.html', {'form':form})










