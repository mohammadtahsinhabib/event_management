from django.db import models

# Create your models here.

class Employee(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES=[
        {"PENDING","Pending"},
        {"IN_PROGRESS","In Progress"},
        {"COMPLETED","Completed"}
    ]

    project = models.ForeignKey("Project",on_delete=models.CASCADE,default=1)
    assigned_to = models.ManyToManyField(Employee)

    title = models.CharField(max_length=250)
    descriptions = models.TextField()
    due_date=models.DateField()
    is_completed = models.BooleanField(default=False)
    status=models.CharField(max_length=15,choices=STATUS_CHOICES,default="PENDING")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class TaskDetails(models.Model):
    HIGH,MEDIUM,LOW="H","M","L"
    PRIORITY_OPTIONS=(
        (HIGH, "High"),
        (MEDIUM,"Medium"),
        (LOW,"Low"),
    )
    
    task=models.OneToOneField(Task,on_delete=models.CASCADE,related_name="details")
    # assigned_to=models.CharField(max_length=250)
    priority=models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW,)
    notes=models.TextField(blank=True,null=True)


    def __str__(self):
        return f"Details form of {self.task.title}"

class Project(models.Model):
    name =models.CharField(max_length=250)
    descriptions = models.TextField(blank=True,null=True)
    start_date = models.DateField()


    def __str__(self):
        return self.name

