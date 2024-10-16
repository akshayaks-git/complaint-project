from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect,render_to_response,redirect
from django.db import connection
from datetime import date
from Complaintapp.forms import profileform
from Complaintapp.models import user_profile_model
from Complaintapp.forms import pform
from Complaintapp.models import promodel
#import googlemaps
import json
from django.conf import settings
def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')
def index(request):
    return render(request,'index.html')
def villages(request):
    return render(request,'villages.html')
def officer(request):
    return render(request,'officer.html')
def category(request):
    return render(request,'category.html')
def cataction(request):
    cursor=connection.cursor()
    catename=request.GET['catename']
    sql="insert into tbl_category(cname)values('%s')"%(catename)
    cursor.execute(sql)
    return render(request,'adminhome.html')
def categoryview(request):
    cursor=connection.cursor()
    sql="select * from  tbl_category"
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'cid':row[0],'cname':row[1]}
        cr.append(x)
    return render(request,'categoryview.html',{'cr':cr})
def cdel(request):
    cursor=connection.cursor()
    id=request.GET['id']
    sql="delete from tbl_category where cid='%s'"%(id)
    cursor.execute(sql)
    message="<script>alert('Deleted Successfully');window.location='/categoryview/';</script>"
    return HttpResponse(message)
def officeraction(request):
    cursor=connection.cursor()
    officername=request.GET['offname']
    Address=request.GET['address']
    Phoneno=request.GET['phoneno']
    emailid=request.GET['email']
    gender=request.GET['gender']
    password=request.GET['password']
    ut="Officer"
    v="insert into tbl_officer(oname,oadr,ophno,oem,gend)values('%s','%s','%s','%s','%s')"%(officername,Address,Phoneno,emailid,gender)
    cursor.execute(v)
    m="select max(oid) as id from tbl_officer"
    cursor.execute(m)
    y=cursor.fetchall()
    for r in y:
        n="insert into tbl_login(uid,uname,upass,utype)values('%s','%s','%s','%s')"%(r[0],emailid,password,ut)
        cursor.execute(n)    
    return render(request,'adminhome.html')
def villagesaction(request):
    cursor=connection.cursor()
    name=request.GET['name']
    Address=request.GET['address']
    wardno=request.GET['wno']
    houseno=request.GET['Hno']
    aadhar=request.GET['adhar']
    Phoneno=request.GET['phno']
    emailid=request.GET['email']
    password=request.GET['pass']
    dte=date.today()
    r="insert into tbl_villages(vname,vadr,wno,hno,phno,em,dte)values('%s','%s','%s','%s','%s','%s','%s')"%(name,Address,wardno,houseno,Phoneno,emailid,dte)
    cursor.execute(r)
    ut='villages'
    sql="select max(vid) as id from tbl_villages"
    cursor.execute(sql)
    cr=[]
    rs= cursor.fetchall()
    for row in rs:
        q="insert into tbl_login(uid,uname,upass,utype)values('%s','%s','%s','%s')"%(row[0],emailid,password,ut)
        cursor.execute(q)
        return render(request,'login.html')

def complaint(request):
    cursor=connection.cursor()
    id=request.session['uid']
    sql="select * from tbl_villages where vid='%s'"%(id)
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'vid':row[0],'vname':row[1],'vadr':row[2],'wno':row[3],'hno':row[4],'phno':row[5],'em':row[6],'dte':row[7]}
        cr.append(x)
    return render(request,'complaint.html',{'cr':cr})
def complaintaction(request):
    
    if request.method == "POST":
        Engform = profileform(request.POST,request.FILES)
        if Engform.is_valid():
            profile =user_profile_model()
            profile.cname=Engform.cleaned_data["cname"]
            profile.complaint=request.POST['complaint']
            profile.p_image=Engform.cleaned_data['p_image']
            profile.uid=request.POST['uid']
            profile.name=request.POST['name']  
            profile.hno=request.POST['hno']
            profile.wno=request.POST['wno']
            profile.status=request.POST['status']
            profile.dte=request.POST['dte']
            profile.location=request.POST['location']
            profile.save()   
            html="<script>alert('Successfully added');window.location='/villagehome/';</script>"
            saved = True
    else:
        Engform = profileform()
    return HttpResponse(html) 
def loginaction(request):
    cursor=connection.cursor()
    uname=request.GET['t1']
    upass=request.GET['t2']
    sql=" select * from tbl_login where uname='%s'and upass='%s'"%(uname,upass)
    cursor.execute(sql)
    cr=[]
    if(cursor.rowcount)>0:
        rs=cursor.fetchall()
        for row in rs:
            request.session['uid']=row[0]
            request.session['utype']=row[3]
        if(request.session['utype']=='admin'):
            return render(request,'adminhome.html')
        elif(request.session['utype']=='villages'):
            return render(request,'villagehome.html')
        elif(request.session['utype']=='Officer'):
            return render(request,'officerhome.html')
    else:
        msg="<script>alert('Invalid username or password');window.location='/index/';</script>"
        return HttpResponse(msg)
        # if (cursor.rowcount)>0:
        #    request.session['uid']=row[0]
        #    request.session['uname']=row[1]
          
        #    request.session['utype']=row[3]
        #    if(request.session['utype']=='Officer'):
        #         request.session['uid']=row[0]
        #         #uid=request.session['id']
        #         return render(request,'officerhome.html')
        #    elif(request.session['utype']=='villages'):
        #         request.session['uid']=row[0]
        #         #uid=request.session['uid']
        #         return render(request,'villagehome.html')
        #    elif(request.session['utype']=='admin'):
        #         request.session['uid']=row[0]
                
        #         return render(request,'adminhome.html')
        # else:
        #     message="<script>alert('login credential invalid');window.location='/login/';</script>"
        #     return HttpResponse(message)

            
def villagesview(request):
    cursor=connection.cursor()
    sql="select * from tbl_villages"
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'vid':row[0],'vname':row[1],'vadr':row[2],'wno':row[3],'hno':row[4],'phno':row[5],'em':row[6]}
        cr.append(x)
    return render(request,'villagesview.html',{'cr':cr})
def officerview(request):
    cursor=connection.cursor()
    sql="select * from tbl_officer"
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'oid':row[0],'oname':row[1],'oadr':row[2],'ophno':row[3],'oem':row[4],'gen':row[5]}
        cr.append(x)
    return render(request,'officerview.html',{'cr':cr})
def odel(request):
    cursor=connection.cursor()
    id=request.GET['id']
    sql="delete from tbl_officer where oid='%s'"%(id)
    cursor.execute(sql)
    message="<script>alert('Deleted Successfully');window.location='/officerview/';</script>"
    return HttpResponse(message)
def complaintview(request):
    cursor=connection.cursor()
    sql="select * from tbl_complaint"
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'cid':row[0],'cname':row[1],'complaint':row[2],'p_image':row[3],'uid':row[4],'name':row[5],'hno':row[6],'wno':row[7],'status':row[8],'dte':row[9],'oid':row[10],'location':row[11]}
        cr.append(x)
    return render(request,'complaintview.html',{'cr':cr})
def adminhome(request):
    return render(request,'adminhome.html')
def officerhome(request):
    cursor=connection.cursor()
    uid=request.session['uid']
    sql="select * from tbl_officer where oid='%s'"%(uid)
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'oid':row[0],'oname':row[1],'oadr':row[2],'ophno':row[3],'oem':row[4],'gen':row[5]}
        cr.append(x)
    return render(request,'officerhome.html',{'cr':cr})
def villagehome(request):
    cursor=connection.cursor()
    uid=request.session['uid']
    sql="select * from tbl_villages where vid='%s'"%(uid)
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'vid':row[0],'vname':row[1]}
        cr.append(x)
    return render(request,'villagehome.html',{'cr':cr})
def viewusers(request):
    cursor=connection.cursor()
    sql="select * from tbl_villages"
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'vid':row[0],'vname':row[1],'vadr':row[2],'wno':row[3],'hno':row[4],'phno':row[5],'em':row[6],'dte':row[7]}
        cr.append(x)
    return render(request,'viewusers.html',{'cr':cr})
def compalintstatus(request):
    cursor=connection.cursor()
    id=request.session['uid']
    sql="select * from tbl_complaint where uid='%s'"%(id)
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        cid=row[0]
        x={'cid':row[0],'cname':row[1],'complaint':row[2],'p_image':row[3],'uid':row[4],'name':row[5],'hno':row[6],'wno':row[7],'status':row[8],'dte':row[9],'oid':row[10]}
        cr.append(x)
    sq="select * from tbl_status where uid='%s' "%(id)
    cursor.execute(sq)
    crr=[]
    rt=cursor.fetchall()
    for rw in rt:
        y={'sid':rw[0],'cid':rw[1],'oid':rw[2],'complaint':rw[3],'stype':rw[4],'p_image':rw[6],'dte':rw[5],'uid':rw[7]}
        crr.append(y)
    return render(request,'compalintstatus.html',{'cr':cr,'crr':crr})
def feedback(request):
    cursor=connection.cursor()
    id=request.session['uid']
    sql="select * from tbl_villages where vid='%s'"%(id)
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'vid':row[0],'vname':row[1]}
        cr.append(x)
    return render(request,'feedback.html',{'cr':cr})
def feedbackaction(request):
    cursor=connection.cursor()
    uid=request.GET['uid']
    nm=request.GET['t1']
    f=request.GET['t2']
    dt=date.today()
    sql="insert into tbl_feedback(uid,name,fdback,dte)values('%s','%s','%s','%s')"%(uid,nm,f,dt)
    cursor.execute(sql)
    message="<script>alert('Send Successfully');window.location='/villagehome/';</script>"
    return HttpResponse(message)
def capr(request):
    cursor=connection.cursor()
    id=request.GET['id']
    sql="update tbl_complaint set status='Approve' where cid='%s'"%(id)
    cursor.execute(sql)
    message="<script>alert('Successfully Approved');window.location='/complaintview/';</script>"
    return HttpResponse(message)
def crej(request):
    cursor=connection.cursor()
    id=request.GET['id']
    sql="update tbl_complaint set status='Reject' where cid='%s'"%(id)
    cursor.execute(sql)
    message="<script>alert('Successfully Rejected');window.location='/complaintview/';</script>"
    return HttpResponse(message)

def assign(request):
    cursor=connection.cursor()
    id=request.GET['id']
    sql="select * from tbl_complaint where cid='%s'"%(id)
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'cid':row[0],'cname':row[1],'complaint':row[2],'p_image':row[3],'uid':row[4],'name':row[5],'hno':row[6],'wno':row[7],'status':row[8],'dte':row[9],'oid':row[10]}
        cr.append(x)
    sq="select * from tbl_officer"
    cursor.execute(sq)
    crr=[]
    rst=cursor.fetchall()
    for ro in rst:
        y={'oid':ro[0],'oname':ro[1],'oadr':ro[2],'ophno':ro[3],'oem':ro[4],'gen':ro[5]}
        crr.append(y)
    return render(request,'assign.html',{'cr':cr,'crr':crr})
def asgnaction(request):
    cursor=connection.cursor()
    id=request.GET['cid']
    nm=request.GET['nm']
    ud=request.GET['ud']
    c=request.GET['t1']
    o=request.GET['t2']
    dt=date.today()
    sql="insert into tbl_assign(cid,name,uid,complaint,oid,dte)values('%s','%s','%s','%s','%s','%s')"%(id,nm,ud,c,o,dt)
    cursor.execute(sql)
    sq="update tbl_complaint set oid='%s' where cid='%s'"%(o,id)
    cursor.execute(sq)
    return render(request,'adminhome.html')
def viewassign(request):
    cursor=connection.cursor()
    uid=request.session['uid']
    sql="select * from tbl_assign where oid='%s'"%(uid)
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'aid':row[0],'cid':row[1],'name':row[2],'uid':row[3],'complaint':row[4],'oid':row[5],'dte':row[6]}
        cr.append(x)
    return render(request,'viewassign.html',{'cr':cr})
def aupdate(request):
    cursor=connection.cursor()
    cid=request.GET['id']
    uid=request.session['uid']
    sql="select * from tbl_complaint where cid='%s' and oid='%s'"%(cid,uid)
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'cid':row[0],'cname':row[1],'complaint':row[2],'p_image':row[3],'uid':row[4],'name':row[5],'hno':row[6],'wno':row[7],'status':row[8],'dte':row[9],'oid':row[10]}
        cr.append(x)
    return render(request,'aupdate.html',{'cr':cr})
# def aupaction(request):
#     cursor=connection.cursor()
#     uid=request.session['uid']
#     id=request.GET['cid']
#     c=request.GET['t1']
#     s=request.GET['t2']
#     sql="update tbl_complaint set status='%s' where cid='%s' and oid='%s'"%(s,id,uid)
#     cursor.execute(sql)
#     return render(request,'officerhome.html')
def viewfeedback(request):
    cursor=connection.cursor()
    sql="select * from tbl_feedback"
    cursor.execute(sql)
    cr=[]
    rs=cursor.fetchall()
    for row in rs:
        x={'fid':row[0],'uid':row[1],'name':row[2],'fdback':row[3],'dte':row[4]}
        cr.append(x)
    return render(request,'viewfeedback.html',{'cr':cr})
def aupaction(request):
    if request.method == "POST":
        Proform = pform(request.POST,request.FILES)
        if Proform.is_valid():
            profile =promodel()
            profile.cid=Proform.cleaned_data["cid"]
            profile.oid=request.POST["oid"]
            profile.complaint=request.POST["complaint"]
            profile.stype=request.POST["stype"]  
            profile.p_image=Proform.cleaned_data["p_image"]
            profile.dte=request.POST["dte"]
            profile.uid=request.POST["uid"]  
            profile.save()   
            html="<script>alert('Successfully added');window.location='/officerhome/';</script>"
            saved = True
    else:
        Proform = pform()
    return HttpResponse(html)
def smpl(request):
    return render(request,'smpl.html')
def sample(request):
    return render(request,'sample.html')
