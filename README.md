# hicarser

Ajax textfile load with async celery worker parsing(count symbols). 
Show progress. 

Stack: django, channels, celery, jquery, websockets. 

```git clone```  
```python manage.py migrate``` 
```celery worker -A hicarser -l info```  
```python manage.py runserver```  
  or for real efficiency:  
```start your wsgi webserver```  
```start your asgi webserver ```  
```edit nginx config```  

Use for your profits.