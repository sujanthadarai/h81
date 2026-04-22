from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)
    email=models.EmailField()
    message=models.TextField()
    
class Category(models.Model):
    title=models.CharField(max_length=200) #veg
    image=models.ImageField(upload_to="images",null=True)
    
    def __str__(self):
        return self.title
    
class Momo(models.Model):
    name=models.CharField(max_length=200) #veg steam momo
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name="items") #Veg
    desc=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2) #4444.00
    image=models.ImageField(upload_to="images")
    
    
    def __str__(self):
        return self.name
    