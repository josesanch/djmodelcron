Generic cron task for running instances of django models
========================================================

What's that?
-------------

Is a library that you can use to attach programmed executions of a
method in the instances of any model in your django applications.


How to use
----------

Install djmodelcron and django-recurrence.


You need to add a generic relation to the cron model of the djmodelcron app.



Using it
---------------

.. code-block:: python
                
   INSTALLED_APPS = (
                ...
                'djmodelcron',
                'recurrence',
   )
  


   # In your models.py
   from djmodelcron.models import Cron
   
   class MyModel(models.Model):
    title = models.CharField(max_length=125)
    cron = generic.GenericRelation(Cron)
   
    def run(self):
     print "This is call every time associated cron is executed"
   
             
      
