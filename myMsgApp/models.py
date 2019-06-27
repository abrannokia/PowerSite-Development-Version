from django.db import models
from django_pandas.managers import DataFrameManager

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=40, verbose_name="first name")
    last_name = models.CharField(max_length=40) #verbose_name will be automatically generated from field name
    # Model method for returning a full name
    
    def _get_full_name(self):
        "Returns a person's full name."
        return '%s %s' % (self.first_name, self.last_name)
    #Add person's full name as a new managed attribute
    full_name = property(_get_full_name)
    # Add a “_str_" method to return the full name of the person in UI
    
    def __str__(self):
        return "{0}".format(self.full_name)
    
    class Product(models.Model):
        product_name=models.TextField()
        objects = models.Manager()
        pdobjects = DataFrameManager()  # Pandas-Enabled Manager 

class Mail (models.Model):
    MAILING_LIST_CHOICES = (
                            ('GO', 'Gina Ortiz'),
                            ('RT', 'Rick Tallon'),
                            ('MF', 'Matt Foster')
                            )
    mail_to = models.CharField(max_length=2, choices=MAILING_LIST_CHOICES, default='GO', verbose_name="Send mail to")
    subject = models.CharField(max_length=150, blank=False)
    mail_date = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE) #many-to-one relationship (one person can send multiple mail messages) #Add a "_str_" method to return more detailed info about an individual message
    def __str__(self):
        return "Message from {0} to {1} on {2}".format(self.person, self.mail_tb, self.mail_date)
    
