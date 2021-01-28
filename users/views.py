from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def register(request):
    """
    Register a bew user
    """
    if request.method != "POST":
        # DISPLAY BLANK FORM
        form = UserCreationForm()
    else:
        # PROCESS COMPLETED FORM
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # log the user in and then redirect to home page.
            login(request,new_user)
            return redirect('blog_app:index')
    # Display a invalid o0r blank form.        
    context = {'form':form}
    return render(request, 'registration/register.html', context)

