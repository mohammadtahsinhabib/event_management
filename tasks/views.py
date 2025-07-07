from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from tasks.forms import TaskModelForm,TaskForm,TaskDetailsModelForm
from tasks.models import Employee,Task
from django.db.models import Count,Q
from django.contrib import messages

def footer(request):
    return render(request,"footer.html")


def manager_dashboard(request):
    type=request.GET.get("type","all")
    tasks=Task.objects.select_related("details").prefetch_related("assigned_to").all()
    
    counts=Task.objects.aggregate(
        total=Count("id"),
        completed=Count("id",filter = Q(status="COMPLETED")),
        progress=Count("id",filter = Q(status="IN_PROGRESS")),
        pending=Count("id",filter = Q(status="PENDING")),
        )
    
    base_queries=Task.objects.select_related("details").prefetch_related("assigned_to")
    if type=="completed":
        tasks = base_queries.filter(status="COMPLETED")
    elif type=="pending":
        tasks = base_queries.filter(status="PENDING")
    elif type=="progress":
        tasks = base_queries.filter(status="IN_PROGRESS")
    else:
        tasks = base_queries.all()
        


    
    context={
        "tasks":tasks,
        "counts":counts
    }
    return render(request,"dashboard/admin_dashboard.html",context)


def user_dashboard(request):
    return render(request,"dashboard/user_dashboard.html")

def create_task(request):
    # employees=Employee.objects.all()
    task_forms=TaskModelForm()
    task_details_forms=TaskDetailsModelForm()

    if request.method=="POST":
        task_forms=TaskModelForm(request.POST)
        task_details_forms=TaskDetailsModelForm(request.POST)

        if(task_forms.is_valid() and task_details_forms.is_valid()):
            task=task_forms.save()
            task_details=task_details_forms.save(commit=False)
            task_details.task=task
            task_details.save()
            messages.success(request,"Task Created Successfully")
            redirect("create-task")
            
    context={"task_form":task_forms,"task_details_form":task_details_forms}
    return render(request,"task_form.html",context)

def update_task(request,id):
    task=Task.objects.get(id=id)
    task_forms=TaskModelForm(instance=task)
    if task.details:
        task_details_forms=TaskDetailsModelForm(instance=task.details)

    if request.method=="POST":
        task_forms=TaskModelForm(request.POST)
        task_details_forms=TaskDetailsModelForm(request.POST,instance=task.details)

        if(task_forms.is_valid() and task_details_forms.is_valid()):
            task_forms.save()
            task_details_forms=task_details_forms.save(commit=False)
            task_details_forms.task=task
            task_details_forms.save()
            messages.success(request,"Task Updated Successfully")
            redirect("create-task")
            
    context={"task_form":task_forms,"task_details_form":task_details_forms}
    return render(request,"task_form.html",context)


def delete_task(request,id):
    if request.method == "POST":
        task=get_object_or_404(task,id=id)
        task.delete()
        messages.success(request,"Task Deleted SuccessFully")

        return redirect("manager-dashboard")
    else:
        messages.error(request,"Something Went Wrong")
        return redirect("manager-dashboard")


def view_task(request):
    tasks = Task.objects.all()
    return render(request,"view_task.html",context={"tasks":tasks})    
