from django.db import models

# Create your models here.
from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Will store hashed passwords

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.password.startswith('pbkdf2_sha256$'):  # Avoid double hashing
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

    
# class LostItem(models.Model):
#     item_name = models.CharField(max_length=255)
#     item_descr = models.CharField(max_length=255)
#     # reg_no = models.CharField(max_length=20)

#     def __str__(self):
#         return f"{self.item_name} - {self.item_descr}"

# class FoundItem(models.Model):
#     item_name = models.CharField(max_length=255)
#     item_descr = models.CharField(max_length=255)
#     # reg_no = models.CharField(max_length=20)

#     def __str__(self):
#         return f"{self.item_name} - {self.item_descr}"
# Model to represent lost items
class LostItem(models.Model):
    item_name = models.CharField(max_length=255)  # Name of the lost item
    item_descr = models.CharField(max_length=255)  # Description of the lost item
    date_lost = models.DateField(null=True, blank=True)  # Automatically adds the date the item was lost
    owner_name = models.CharField(max_length=255, null=True, blank=True)  # Name of the person who lost the item
    owner_contact = models.CharField(max_length=15, null=True, blank=True)  # Contact information of the owner

    def __str__(self):
        return f"{self.item_name} - {self.item_descr}"

# Model to represent found items
class FoundItem(models.Model):
    item_name = models.CharField(max_length=255)  # Name of the found item
    item_descr = models.CharField(max_length=255)  # Description of the found item
    date_found = models.DateField(null=True, blank=True)  # Automatically adds the date the item was found
    finder_name = models.CharField(max_length=255, null=True, blank=True)  # Name of the person who found the item
    finder_contact = models.CharField(max_length=15, null=True, blank=True)  # Contact information of the finder

    def __str__(self):
        return f"{self.item_name} - {self.item_descr}"
        
class Collaborative(models.Model):
    event_name = models.CharField(max_length=255, blank=True, null=True)
    organizer = models.CharField(max_length=255, blank=True, null=True)  # Optional
    collaboration_descr = models.TextField(blank=True, null=True)
    skills_preferred = models.CharField(max_length=255, blank=True, null=True)
    team_size = models.IntegerField( blank=True, null=True)
    deadline = models.DateField( blank=True, null=True)
    posted_by = models.CharField(max_length=255, blank=True, null=True)  # Can store the user's name or email
    contact_email = models.EmailField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return f"{self.event_name} - {self.organizer}"

class CollaborationRequest(models.Model):
    event_name = models.CharField(max_length=100)
    organizer = models.CharField(max_length=100)
    collaboration_descr = models.TextField()
    skills_preferred = models.CharField(max_length=255)
    team_size = models.IntegerField()
    deadline = models.DateField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_email = models.EmailField()
    
class Application(models.Model):
    collaboration = models.ForeignKey(CollaborationRequest, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')

class Issue1(models.Model):
    issue_name = models.CharField(max_length=255)
    issue_descr = models.CharField(max_length=255)
    # issue_reg = models.CharField(max_length=255)
    comment1 = models.CharField(max_length=255)
    comment2 = models.CharField(max_length=255)
    comment3 = models.CharField(max_length=255)
    comment4 = models.CharField(max_length=255)
    comment5 = models.CharField(max_length=255)
    # comments = ArrayField(models.CharField(max_length=255),size=8)
    # reg_no = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.issue_name} - {self.issue_descr} - {self.comment1} - {self.comment2}- {self.comment3}- {self.comment4}- {self.comment5}"

class Tutor(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    contact = models.CharField(max_length=15, null=True, blank=True)
    payment = models.FloatField()

class TutorWanted(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    contact = models.CharField(max_length=15, null=True, blank=True)
    payment = models.FloatField()

