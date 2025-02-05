from django.db import models
import uuid

# Create your models here.
class BaseModel(models.Model):
    uuid=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)
    createdAt=models.DateField(auto_now=True)
    updatedAt=models.DateField(auto_now_add=True)
    
    class Meta:
        abstract=True  #it will be the base class
        
class Transaction(BaseModel):
    description=models.CharField(max_length=100)
    amount=models.FloatField()
    
    class Meta:
        ordering=('description',)
        
    
    def isNegative(self):
        return self.amount < 0