from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('logpass')  # Confirm password field

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        user = User(username=username, password=password)  # `save()` auto-hashes password
        user.save()

        request.session['username'] = user.username  # Start session
        messages.success(request, "Registration successful!")
        return redirect('home')

    return render(request, "wordleapp/register.html")
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found!")
            return redirect('login')

        if user.check_password(password):  # Secure password checking
            request.session['username'] = user.username
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Incorrect password!")
            return redirect('login')

    return render(request, "wordleapp/login.html")

def home(request):
    return render(request, "wordleapp/home.html")
def land(request):
    return render(request, "wordleapp/user.html")

# View to process the lost item form and add new items
def process_item_lost(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_descr = request.POST.get('item_descr')
        owner_name = request.POST.get('owner_name')
        owner_contact = request.POST.get('owner_contact')
        date_lost = request.POST.get('date_lost')  # Assuming date is sent as a string in the format 'YYYY-MM-DD'

        # Create a new LostItem entry
        item = LostItem(
            item_name=item_name,
            item_descr=item_descr,
            owner_name=owner_name,
            owner_contact=owner_contact,
            date_lost=date_lost if date_lost else None  # Handle empty date
        )
        item.save()

        # Fetch updated items to display
        items_lost = LostItem.objects.all()
        items_found = FoundItem.objects.all()
        return render(request, 'wordleapp/lost_and_found.html', {'items_lost': items_lost, 'items_found' : items_found})

# View to process the found item form and add new items
def process_item_found(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_descr = request.POST.get('item_descr')
        finder_name = request.POST.get('finder_name')
        finder_contact = request.POST.get('finder_contact')
        date_found = request.POST.get('date_found')  # Assuming date is sent as a string in the format 'YYYY-MM-DD'

        # Create a new FoundItem entry
        item = FoundItem(
            item_name=item_name, 
            item_descr=item_descr,
            finder_name=finder_name,
            finder_contact=finder_contact,
            date_found=date_found if date_found else None  # Handle empty date
        )
        item.save()

        # Fetch updated items to display
        items_lost = LostItem.objects.all()
        items_found = FoundItem.objects.all()
        return render(request, 'wordleapp/lost_and_found.html', {'items_lost': items_lost, 'items_found' : items_found})

def process_issue(request):
    if request.method == 'POST':
        issue_name = request.POST.get('issue_name')
        issue_descr = request.POST.get('issue_descr')
        # Create a new patient entry in the database using the Patient model
        issue = Issue1(issue_name=issue_name, issue_descr=issue_descr)
        issue.save()
        issues=Issue1.objects.all()
        return render(request, 'wordleapp/issue_central.html', {'issues' : issues})

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Collaborative
from wordleapp.forms import CollaborationForm
from django.contrib import messages

def process_collaboration(request):
    if request.method == 'POST':
        form = CollaborationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Collaboration request posted successfully!")
            return redirect('collaboration')
        else:
            messages.error(request, "Error in form submission. Please check your inputs.")
    else:
        form = CollaborationForm()

    return render(request, "wordleapp/collaboration_form.html", {"form": form})

def collaboration(request):
    collabs_list = Collaborative.objects.all().order_by('-created_at')
    
    # Pagination settings
    paginator = Paginator(collabs_list, 5)  # Show 5 collaborations per page
    page_number = request.GET.get('page')
    collabs = paginator.get_page(page_number)

    return render(request, 'wordleapp/collaboration.html', {'collabs': collabs})

def collaboration_form(request):
    form = CollaborationForm()
    return render(request, "wordleapp/collaboration_form.html", {"form": form})

from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Collaborative
import os

def submit_resume(request):
    if request.method == "POST" and request.FILES.get("resume"):
        collab_id = request.POST.get("collab_id")
        collab = get_object_or_404(Collaborative, id=collab_id)

        resume_file = request.FILES["resume"]
        
        # Save file to media directory (inside /media/resumes/)
        resume_path = f"resumes/{resume_file.name}"
        file_path = default_storage.save(resume_path, resume_file)
        file_url = f"{settings.MEDIA_URL}{file_path}"  # URL to access file

        # Email with a download link
        send_mail(
            subject=f"New Collaboration Request for {collab.event_name}",
            message=(
                f"A user has submitted their resume for {collab.event_name}.\n\n"
                f"Download Resume: {request.build_absolute_uri(file_url)}"
            ),
            from_email="sharvaniakkenapally@gmail.com",
            recipient_list=[collab.contact_email],
            fail_silently=False,
        )

        return JsonResponse({"message": "Resume submitted successfully!"})

    return JsonResponse({"message": "Invalid request"}, status=400)

# def collaboration_dashboard(request):
#     collaborations = CollaborationRequest.objects.all()
#     applications = Application.objects.filter(collaboration__in=collaborations)
    
#     return render(request, 'collaboration_dashboard.html', {'collaborations': collaborations, 'applications': applications})

# def update_application_status(request, application_id, status):
#     application = Application.objects.get(id=application_id)
#     application.status = status
#     application.save()
    
#     return redirect('collaboration_dashboard')
from django.contrib.auth.decorators import login_required

@login_required
def collaboration_detail(request, collaboration_id):
    # Get the collaboration post
    collaboration = get_object_or_404(CollaborationRequest, id=collaboration_id)
    
    # Check if the logged-in user is the author of the collaboration post
    if collaboration.posted_by != request.user:
        # If the user is not the author, redirect or show a permission error
        return redirect('collaboration_dashboard')
    
    # Get the applications related to this collaboration
    applications = Application.objects.filter(collaboration=collaboration)

    return render(request, 'collaboration_detail.html', {'collaboration': collaboration, 'applications': applications})

@login_required
def update_application_status(request, application_id, status):
    application = get_object_or_404(Application, id=application_id)
    # Ensure the current user is the author of the collaboration post
    if application.collaboration.posted_by != request.user:
        return redirect('collaboration_dashboard')
    
    # Update the application status
    application.status = status
    application.save()
    
    return redirect('collaboration_detail', collaboration_id=application.collaboration.id)

def process_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        issue_id = request.POST.get('issue_id')
        # print(comment, issue_id)
        # Create a new patient entry in the database using the Patient model
        for i in Issue1.objects.filter(id__in=issue_id):
            print(i.comment1, i.comment2)
            if i.comment1=="":
                i.comment1=comment
            elif i.comment2=="":
                i.comment2=comment
            elif i.comment3=="":
                i.comment3=comment
            elif i.comment4=="":
                i.comment4=comment
            elif i.comment5=="":
                i.comment5=comment


            i.save()
        issues=Issue1.objects.all()
        return render(request, 'wordleapp/issue_central.html', {'issues' : issues})

def lost_and_found(request):
    items_lost = LostItem.objects.all()
    items_found = FoundItem.objects.all()
    return render(request, 'wordleapp/lost_and_found.html', {'items_lost': items_lost, 'items_found' : items_found})
# View to render the lost item form page
def lost_form(request):
    return render(request, "wordleapp/lost_form.html")

# View to render the found item form page
def found_form(request):
    return render(request, "wordleapp/found_form.html")
def issue_form(request):
    return render(request, "wordleapp/issue_form.html")



def issue_central(request):
    if request.method == 'POST':
        issue_name = request.POST.get('issue_name')
        issue_descr = request.POST.get('issue_descr')
        # Create a new patient entry in the database using the Patient model
        issue = Issue1(issue_name=issue_name, issue_descr=issue_descr)
        issue.save()
    issues = Issue1.objects.all()
    return render(request, "wordleapp/issue_central.html", {'issues' : issues})

def peertutor(request):
    context = {
        'tutors' : Tutor.objects.all(), 
        'tutors_wanted' : TutorWanted.objects.all()
    }

    return render(request, "wordleapp/peertutor.html", context)

def tutorform(request):
    return render(request, "wordleapp/tutorform.html")

def tutorwantedform(request):
    return render(request, "wordleapp/tutorwantedform.html")

def add_tutor(request):
    if request.method == 'POST':
        tutor = Tutor(
            name = request.POST.get('name'),
            subject = request.POST.get('subject'),
            payment = request.POST.get('payment'),
            contact = request.POST.get('contact')
        )

        tutor.save()

        context = {
            'tutors' : Tutor.objects.all(), 
            'tutors_wanted' : TutorWanted.objects.all()
        }

        return render(request, "wordleapp/peertutor.html", context)
    
def add_tutor_wanted(request):
    if request.method == 'POST':
        tutorwanted = TutorWanted(
            name = request.POST.get('name'),
            subject = request.POST.get('subject'),
            payment = request.POST.get('payment'),
            contact = request.POST.get('contact')
        )

        tutorwanted.save()

        context = {
            'tutors' : Tutor.objects.all(), 
            'tutors_wanted' : TutorWanted.objects.all()
        }

        return render(request, "wordleapp/peertutor.html", context)



