# hicarser

Ajax textfile load,parse(count symbols) with celery task, save result to db. 
Show progressing on each step. 

Stack: django, channels, celery, jquery, websockets. 

```git clone```  
```python manage.py migrate```  
```celery worker -A hicarser -l info```  
```python manage.py runserver```  
  or for real efficiency:  
```start your wsgi webserver (gunicorn for example)```  
```start your asgi webserver (daphne for example)```  
```edit your nginx config (hicarser.conf for example)```  

Use for your profits.

Possible improvements:
- drag'n'drop file to upload  
- multiple files upload  
- config celery for several workers  
- check file saving status  
- alter client-side with React  
- for production use industrial database (MySQL, PostgreSQL)  
