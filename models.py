from django.db import models
class user_profile_model(models.Model):
    cname=models.CharField(max_length=20)
    complaint=models.CharField(max_length=500)
    p_image=models.FileField(upload_to='pictures')
    uid=models.CharField(max_length=50)   
    name=models.CharField(max_length=250)
    hno=models.CharField(max_length=200)  
    wno=models.CharField(max_length=100) 
    status=models.CharField(max_length=100)
    dte=models.CharField(max_length=10)
    location=models.CharField(max_length=50)
    class Meta:
        db_table="tbl_complaint"
class promodel(models.Model):
    cid=models.CharField(max_length=20)
    oid=models.CharField(max_length=20)
    complaint=models.CharField(max_length=200)
    stype=models.CharField(max_length=50)      
    p_image=models.FileField(upload_to='pictures')
    dte=models.CharField(max_length=50)
    uid=models.CharField(max_length=50)  
    class Meta:
        db_table="tbl_status"
