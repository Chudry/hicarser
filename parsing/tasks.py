from __future__ import absolute_import
import datetime
import json
import os

from channels import Group

from hicarser.celery import app
from .models import TextFile


@app.task
def process_file(file_id):
    """TextFile processing.

    Get TextFile, open storing file,
    count symbols line by line, char by char,
    every '1% progress' send websocket message to client,
    save result to TextFile,
    send websocket message to client with result.

    Decorators:
        app.task

    Arguments:
        file_id {int} -- TextFile id
    """
    file = TextFile.objects.get(pk=file_id)
    with open(file.file) as f:
        size = os.fstat(f.fileno()).st_size
        step = size // 100
        result = 0
        for line in f:
            for char in line:
                result += 1
                if result % step == 0:
                    Group('pool').send({
                        "text": json.dumps({
                            "action": "processing",
                            "file_id": file_id,
                            "progress": result // step,
                        })
                    })

    file.amount = result
    file.completed = datetime.datetime.now()
    file.save()
    Group('pool').send({
        "text": json.dumps({
            "action": "completed",
            "file_id": file_id,
            "file_amount": result,
        })
    })
