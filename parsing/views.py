import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from channels import Group

from hicarser.settings import BASE_DIR

from .models import TextFile
from .tasks import process_file


def index(request):
    """Index page view.

    Move all textfiles to context.
    """
    files = TextFile.objects.all()
    return render(request, 'index.html', {'files': files})


def handle_file(file):
    """Get temporary uploaded file and write it into 'project/upload/' dir.

    Returns:
        tuple -- file path, file name
    """
    destination = BASE_DIR + '/upload/' + file.name
    with open(destination, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
    return (destination, file.name)


@csrf_exempt
def upload(request):
    """Upload function.

    Take ajax request, handle file, save it to db,
    send websocket message to client for table change,
    then start 'process_file' celery task.

    Decorators:
        csrf_exempt

    Returns:
        json -- don't need it.
    """
    if request.is_ajax():
        data = {}
        destination, name = handle_file(request.FILES.values()[0])
        textfile = TextFile()
        textfile.name = name
        textfile.file = destination
        textfile.save()
        Group('pool').send({
            "text": json.dumps({
                "action": "uploaded",
                "file_id": request.FILES.keys()[0],
                "new_file_id": textfile.id,
            })
        })
        process_file.delay(textfile.id)
        data = {'msg': 'Success'}
    else:
        data = {'msg': 'Failed'}
    return JsonResponse(data)
