from django import forms
from django.forms import CharField
from Complaintapp.models import user_profile_model
from Complaintapp.models import promodel

class pform(forms.Form):
    cid=forms.CharField(max_length=20)
    p_image=forms.FileField()
    class Meta:
        model = promodel
        fields = ['cid','oid','complaint','stype','dte','p_image','uid']
class profileform(forms.Form):
    cname=forms.CharField(max_length=100)
    complaint=forms.CharField(max_length=500)
    p_image=forms.FileField()
    
    class Meta:
        model = user_profile_model
        fields = ['cname','complaint','p_image','uid','name','hno','wno','status','dte','oid','location']
