from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Google Cloud Imports
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
import datetime, json, time, google.auth.transport.requests, google.oauth2.id_token

# Setting Project and Parameters

def index(request):
    csrf_token = request.COOKIES.get('csrftoken')
    blogdetails = cloudTaskBlog.objects.all().reverse()[:5]
    return render(request,'ct_templates/index.html',{'blog':blogdetails})

def create_task(request):
    #Create CSRF token
    csrf_token = request.COOKIES.get('csrftoken')
    project = '' #GCP Project
    location = 'us-central1'
    queue = 'my-appengine-queue'
    payload = '{"payload":"Hello World"}'
    in_seconds = 30
    deadline = 900

    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(project, location, queue)
    #my_url = 'https://cs-us-central1-brqy.cloudshell.dev/cloudtasks/process_task'
    my_url = 'https://project-name.uc.r.appspot.com/cloudtasks/process_task'
    task = {
        'http_request': {  # Specify the type of request.
            'http_method': tasks_v2.HttpMethod.POST,
            'url': my_url
        }
    }
    if payload is not None:
        if isinstance(payload, dict):
            # Convert dict to JSON string
            payload = json.dumps(payload)
            # specify http content-type to application/json
            task["http_request"]["headers"] = {"Content-type": "application/json", "X-CSRFToken":csrf_token}
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task['http_request']['body'] = converted_payload

    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        d = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=in_seconds)

        # Create Timestamp protobuf.
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(d)

        # Add the timestamp to the tasks.
        task['schedule_time'] = timestamp
    # Use the client to build and send the task.
    response = client.create_task(parent=parent, task=task)
    #print('Created task {}'.format(response.name))
    #return render(request,'ct_templates/ct_task.html',{'task_response': response})
    return JsonResponse(response.name,  safe=False)

@csrf_exempt
def task_handler(request):
    if request.method == "POST":
        """Log the request payload."""
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        payload = body['payload']
        print('Received task with payload: {}'.format(payload))
        response = "Received task with payload: "+ payload
    return render(request,'ct_templates/process_task.html',{'task_response': response})

def create_task_cf(request):
    project = '' #GCP Project
    location = 'us-central1'
    queue = 'my-appengine-queue'
    payload = '{"payload":"This is Cloud Function test with Cloud Task"}'
    in_seconds = 0
    deadline = 900
    audience="https://task-function-uc.a.run.app"
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)
    bearer_token = "bearer " + id_token
    #print(bearer_token)

    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(project, location, queue)
    #'url': 'https://us-central1-brqy.cloudshell.dev/cloudtasks/process_task'
    task = {
        'http_request': {  # Specify the type of request.
            'http_method': tasks_v2.HttpMethod.POST,
            'url': 'https://project-name.uc.r.appspot.com/webapp/',
            "oidc_token": {
            "service_account_email": "compute@developer.gserviceaccount.com",
            "audience": "https://project-name.uc.r.appspot.com/webapp/",
        },
        }
    }
    if payload is not None:
        if isinstance(payload, dict):
            # Convert dict to JSON string
            payload = json.dumps(payload)
            # specify http content-type to application/json
            task["http_request"]["headers"] = {"Content-type": "application/json", "Authorization":id_token}
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task['http_request']['body'] = converted_payload

    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        d = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=in_seconds)

        # Create Timestamp protobuf.
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(d)

        # Add the timestamp to the tasks.
        task['schedule_time'] = timestamp

    # Use the client to build and send the task.
    response = client.create_task(parent=parent, task=task)
    print('Created task {}'.format(response.name))
    return HttpResponse(status=200)

def wait_time(request):
    time.sleep(int(request.GET.get('time')))
    blogdetails = cloudTaskBlog.objects.all().reverse()[:5]
    return render(request,'ct_templates/index.html',{'blog':blogdetails})