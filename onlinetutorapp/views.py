from distutils.log import info
from pydoc_data import topics
from django.core.mail import send_mail
from django.db import connection
from django.shortcuts import render, redirect
from onlinetutorapp.models import Coursematerial, Coursesubject, Discussion, Helpdesk, Homepage, Todolist, User, Userrole, Role
from .forms import FormAddMaterial, FormForgotPassword, FormHelpdesk, FormTodolist, FormUser, FormUserLogin, FormEditMaterial, FormDiscussion, FormDiscussioncomment, FormQuestionselection, FormQuiz, FormQuizquestion
from django.contrib import messages
from django.http import FileResponse
import os

# Create your views here.
# request -> response
# request handler / action

#Functions below: HOME PAGE
def mainpage(request):
    info = gethomeinfo()
    context = {'currenttitle' : info.title, 'file1url' : info.file1, 'file2url' : info.file2}
    return render(request, "mainpage.html", context)

def mainpage_user(request):
    info = gethomeinfo()
    context = {'currenttitle' : info.title, 'file1url' : info.file1, 'file2url' : info.file2}
    return render(request, "mainpage_user.html", context)

def showedithomepagebutton_mainpage_user(request, userid):
    info = gethomeinfo()
    userrole = get_userrole(userid)
    context = {'userid' : userid, 'currenttitle' : info.title, 'file1url' : info.file1, 'file2url' : info.file2, 'roleid' : userrole.roleid_id}
    return render(request, 'mainpage_user.html', context)

def get_userrole(userid):
    userid = userid
    content = Userrole.objects.raw('SELECT * FROM userrole WHERE userid = userid limit 1')
    for userrole in content:
        return userrole

def gethomeinfo():
    info = Homepage.objects.get(id = 1)
    return info

def edithomepage(request):
    info = gethomeinfo()
    context = {'currenttitle' : info.title, 'file1url' : info.file1, 'file2url' : info.file2}
    if request.method == 'POST':
        if (request.POST.get('newurl') != '') and (request.POST.get('file') == 'file1' or request.POST.get('file') == 'file2'):
            if request.POST.get('file') == 'file1':
                Homepage.objects.filter(id=1).update(file1 = request.POST.get('newurl'))
            elif request.POST.get('file') == 'file2':
                Homepage.objects.filter(id=1).update(file2 = request.POST.get('newurl'))
            messages.success(request, "Home Page information updated successfully.")
            info = gethomeinfo()
            context = {'currenttitle' : info.title, 'file1url' : info.file1, 'file2url' : info.file2}
            return render(request, 'edithomepage.html', context)
        else:
            messages.error(request, "Your information is invalid.")
    return render(request, 'edithomepage.html', context)

# Functions below: REGISTER
# Lau Wan Jing: https://www.tutorialspoint.com/how-to-add-a-captcha-in-a-django-website -- captcha 
# Lau Wan Jing: https://www.youtube.com/watch?v=mOS0L5Lb2u0&ab_channel=Desphixs --register function
def register(request):
    if request.method == "POST":
        form = FormUser(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data.get('name')
            staffid = form.cleaned_data.get('staffid')
            get_email_pass(staffid)
            form.save()
            insertrole(staffid)
            messages.success(request, f"Hi {fullname}, your account was created successfully! Please check your email for your password.")
            return redirect('login')
    else:
        form = FormUser()
    return render(request, 'register.html', {'form': form})

def get_email_pass(staffid):
    x = staffid
    content = User.objects.raw('SELECT * FROM user WHERE staffid = %s limit 1', [x])
    for user in content:
        sendemail(user)

# Lau Wan Jing: https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
def sendemail(user):
    subject = 'Welcome to E-Tutor!'
    message = f'Hi {user.staffid}, thank you for registering in E-Tutor web page. Your password is {user.password} and you can sign in into the account now.'
    email_from = "ebook4006@gmail.com"
    recipient_list = [user.email]
    send_mail( subject, message, email_from, recipient_list )

# Lau Wan Jing: https://stackoverflow.com/questions/37839867/django-error-cannot-assign-must-be-an-instance
def insertrole(staffid):
    userrole= Userrole.objects.create(userid = User.objects.get(staffid = staffid), roleid = Role.objects.get(name = 'student'))
    userrole.save()

# Functions below: LOGIN
# Lau Wan Jing: https://itsourcecode.com/free-projects/python-projects/django-login-and-registration-with-source-code/
# Lau Wan Jing: https://ordinarycoders.com/blog/article/django-user-register-login-logout
# Lau Wan Jing: https://pythonprogramming.net/user-login-logout-django-tutorial/
def login(request):
    if request.method == 'POST':
        staffid = request.POST.get('staffid')
        password = request.POST.get('password') 
        #django requires validation
        if ((staffid == None) or (password == None)):
            messages.error(request, 'Empty Staff ID/Password')
        else:
            user = User.objects.get(staffid = staffid, password =password)
            if (not(user)):
                messages.error(request, 'Incorrect ID/Password. Please try again')
            else:
                if user.isactive == 1:
                    return redirect('mainpage_user', userid = user.id)
                    #return HttpResponseRedirect(reverse('mainpage_user', args=(user.id,)))
    else:
        form = FormUserLogin(None)
    return render(request, 'login.html', { 'form' : form }) #but jump to here

def get_login(request, staffid, password):
    x = staffid
    y = password
    content = User.objects.raw('SELECT * FROM user WHERE staffid = %s limit 1', [x])
    # Lau Wan Jing: https://stackoverflow.com/questions/1387727/checking-for-empty-queryset-in-django
    if (not(content)):
        messages.error(request, 'Your ID is not found.')
    else:
        for user in content:
            login_verify(request, user, y)

def login_verify(request, user, y):
    if user.isactive == 1:
        if user.password == y:
            messages.success(request, f'Welcome, you are logged in as {user.staffid}.')
            #userid = user.id
            #mainpage_user(request, userid)this?
            return redirect('mainpage_user')
            #return redirect(request.GET.get('next','/'))
        else:
            messages.error(request, 'Your password is incorrect. Please try again.')
    else:
        messages.error(request, 'Your account is inactive.')

# Functions below: FORGOT PASSWORD
def forgotpassword(request):
    if request.method == 'POST':
        form = FormForgotPassword(request.POST)
        email = request.POST.get('email')
        get_forgotpassword(request, email)
        messages.success(request, 'Please check your email for your password.')
        return redirect('login')
    else:
        form = FormUser(None)
    return render(request, 'forgotpassword.html', { 'form' : form })

def get_forgotpassword(request, email):
    content = User.objects.raw('SELECT * FROM user WHERE email = %s limit 1', [email])
    if (not(content)):
        messages.error(request, 'Your email is not found.')
    else:
        for user in content:
            send_email_forgot_password(user)

def send_email_forgot_password(user):
    subject = 'E-Tutor Online Tutor System'
    message = f'Hi {user.name}, Your password is {user.password} and you can sign in into the account now.'
    email_from = "ebook4006@gmail.com"
    recipient_list = [user.email]
    send_mail( subject, message, email_from, recipient_list )

# Functions below: HELPDESK
def helpdesk(request):
    if request.method == 'POST':
        form = FormHelpdesk(request.POST)
        email = request.POST.get('email')
        if form.is_valid():
            form.save()
            get_helpdesk_info(email)
            messages.success(request, 'Thanks for you feedback, system owner will contact you via email.')
        else:
            messages.error(request, 'Your information is invalid. Please try again.')
    else:
        form = FormUser(None)
    return render(request, 'helpdesk.html', { 'form' : form })

def get_helpdesk_info(email):
    content = Helpdesk.objects.raw('SELECT * FROM helpdesk WHERE email = %s limit 1', [email])
    for user in content:
        send_email_helpdesk(user)

def send_email_helpdesk(user):
    subject = 'E-Tutor Online Tutor System'
    message = f'Hi system owner, there is a question from E-Tutor system. From {user.email} and the question is {user.question}'
    email_from = "ebook4006@gmail.com"
    # Lau Wan Jing: https://stackoverflow.com/a/48107308 -- error 'to' argument solved
    send_mail(subject, message, email_from, ["lauwan08@gmail.com"])

# functions below: SETTINGS
def settings(request, userid):
    context = {'userid' : userid}
    if request.method == 'POST':
        #form = FormUser(request.POST)
        currentpassword = request.POST.get('oldpass')
        newpassword = request.POST.get('newpass')
        confirmnewpassword = request.POST.get('connewpass')
        if (request.POST.get('oldpass') != '') and (request.POST.get('newpass') == request.POST.get('connewpass')):
            correctpassword_or_not = password_verify(userid, currentpassword)
            if correctpassword_or_not == "yes":
                if newpassword == confirmnewpassword:
                    #Lau Wan Jing: https://djangobook.com/django-tutorials/mastering-django-models/
                    User.objects.filter(id=userid).update(password=newpassword)
                    messages.success(request, 'Your password is changed successfully, please login with new password next time.')
                    return render(request, 'settings.html')
                else:
                    messages.error(request, 'Your new password and confirm new password are incorrect. Please try again.')
                    return render(request, 'settings.html')
            else:
                messages.error(request, 'Your password is incorrect. Please try again.')
                return render(request, 'settings.html')
        else:
            messages.error(request, 'Your password is invalid. Please try again.')
            return render(request, 'settings.html')
    else:
        return render(request, 'settings.html', context)

def password_verify(userid, currentpassword):
    content = User.objects.raw('SELECT * FROM user WHERE id = %s limit 1', [userid])
    for user in content:
        if currentpassword == user.password:
            return str("yes")
        else:
            return str("no")

def getinfotodolist(userid):
    try:
        info = Todolist.objects.get(userid = userid)
        context = {'id' : info.id, 'userid' : info.userid, 'task' : info.task, 'timeend' : info.timeend, 'status' : info.status}
        return context
    except Todolist.DoesNotExist:
        return None


#add: reminder function






#status changes in checkbox
def checkbox(context):
    if context.info.status == 1:
        Todolist.objects.filter(id=context.status).update(status = 0)
    else:
        Todolist.objects.filter(id=context.status).update(status = 1)

def todolist(request, userid):
    #get tasks
    context = getinfotodolist(userid)
    if context is not None:
        #deletetask
        if request.POST.get('delete'):
            deletetask(request, context)
        #edit task status
        elif request.POST.get('checkbox'):
            checkbox(context)
        #add task
        elif request.method == 'POST':
            form = FormTodolist(request.POST)
            #task = request.POST.get('task')
            #timeend = request.POST.get('timeend')
            if form.is_valid():
                #add = todolist(task=task,timeend=timeend)
                #ERROR
                newtask = Todolist.objects.create(User.objects.get(id = userid), task = request.POST.get('task'), timeend = request.POST.get('timeend'))
                newtask.save()
                #get latest data
                context = getinfotodolist(userid)
                return render(request, "todolist.html", context)
            else:
                messages.error(request, 'Your information is invalid. Please try again.')
        else:
        #show tasks
            form = FormTodolist(None)
        return render(request, 'todolist.html', context)
    else:
        return render(request, 'todolist.html', context)

def deletetask(request, context):
    task = Todolist.objects.get(id=context.id)
    task.delete()
    userid = context.userid
    context = getinfotodolist(userid)
    return render(request, 'todolist.html', context)

#Lau Wan Jing: get course subject from coursesubject table
def getcourselistinfo(userid):
    info = Coursesubject.objects.get(id=1)
    context = {'name': info.name, 'userid' : userid}
    return context

def courselist(request, userid):
    subject = getcourselistinfo(userid)
    ##Lau Wan Jing: join userid and subject into the context and pass to html
    subject['userid'] = userid
    return render(request, "courselist.html", subject)

def getcoursematerialinfo():
    #Lau Wan Jing: https://stackoverflow.com/a/61908629 -- fetch all data from coursematerial table
    cursor = connection.cursor()
    query = "Select * from coursematerial WHERE isactive=1"
    cursor.execute(query)
    list = [list for list in cursor.fetchall()]
    return list

def getcoursepageinfo(request):
    materialinfo = getcoursematerialinfo()
    info = {'materialinfo' : materialinfo}
    return (request, info)

def coursepage(request, userid):
    userrole = get_userrole(userid)
    list = getcoursematerialinfo()
    context = {'userid' : userid, 'roleid' : userrole.roleid_id, 'list' : list}
    if request.method == 'POST':
        if request.POST.get('Edit'):
            return redirect(request, "editmaterials.html")
        elif request.POST.get('Delete Materials'):
            return redirect(request, "deletematerials.html")
        elif request.POST.get('Add Materials'):
            return redirect(request, "addmaterials.html")
    else:
        form = FormUser(None)
    context['form'] = form
    return render(request, 'coursepage.html', context)

def addmaterials(request, coursesubjectid):
    if request.method == 'POST':
        form = FormAddMaterial(request.POST)
        if form.is_valid():
            newmaterials = Coursematerial.objects.create(coursesubjectid = Coursesubject.objects.get(id=coursesubjectid), title = request.POST.get('title'), description = request.POST.get('description'), file = request.POST.get('file'))
            newmaterials.save()
            messages.success(request, 'Subject materials added successfully.')
            return redirect(request, "addmaterials.html")
        else:
            messages.error(request, 'Information invalid, please try again.')
    else:
        form = FormAddMaterial(None)
        return render(request, 'addmaterials.html')

def editmaterials(request, coursesubjectid):
    if request.method == 'POST':
        form = FormEditMaterial(request.POST)
        if form.is_valid():
            editmaterials = Coursematerial.objects.create(coursesubjectid = Coursesubject.objects.get(id=coursesubjectid), title = request.POST.get('title'), description = request.POST.get('description'), file = request.POST.get('file'))
            editmaterials.save()
            messages.success(request, 'Subject materials edited successfully.')
            return redirect(request, "editmaterials.html")
        else:
            messages.error(request, 'Your information is invalid. Please try again.')
    else:
        form = FormEditMaterial(None)
        return render(request, 'editmaterials.html')

def getdeletematerialsinfo(userid):
    try:
        info = Coursematerial.objects.get(userid = userid)
        context = {'id' : info.id, 'subject' : info.subject, 'title' : info.title}
        return context
    except Coursematerial.DoesNotExist:
        return None

def deletematerials(request, coursesubjectid):
    if request.method == 'POST':
        form = Coursematerial(request.POST)
        if form.is_valid():
            delete = Coursematerial.objects.create(coursesubjectid = Coursesubject.objects.get(id=coursesubjectid), title = request.POST.get('title'))
            delete.save()
            messages.success(request, 'Subject materials deleted successfully.')
            return redirect(request, "deletematerials.html")
        else:
            messages.error(request, 'Your information is invalid. Please try again.')
    else:
        form = Coursematerial(None)
        return render(request, 'deletematerials.html')

# delete materials the up one or this one
def deletematerials(request, context):
    materials = Coursematerial.objects.get(id=context.id)
    materials.delete()
    userid = context.userid
    context = getdeletematerialsinfo(userid)
    return render(request, 'deletematerials.html', context)

def getdiscussionboardinfo():
    info = Discussion.objects.get(id=1)
    context = {'discussion': info.discussion}
    return context

def discussionboard(request, userid):
    discuss = getdiscussionboardinfo(userid)
    discuss['userid'] = userid
    return render(request, "discussionboard.html", discuss)

def discussionquestion(request):
    if request.method == 'POST':
        form = FormDiscussion(request.POST)
        question = request.POST.get('question')
        description = request.POST.get('description')
        file = request.POST.get('file')
        add = discussionquestion(question=question,description=description,file=file)
        add.save()
        return render(request,"discussionquestion.html",{'add':add})
    else:
        form = FormDiscussion(None)
    return render(request, 'discussionquestion.html', { 'form' : form })

def addquestion(request):
    if request.method == 'POST':
        form = FormDiscussion(request.POST)
        if form.is_valid():
            form.save()
            question = request.POST.get('question')
            description = request.POST.get('description')
            file = request.POST.get('file')
            add = addquestion(question=question,description=description,file=file)
            add.save()
            messages.success(request, 'Question Added Successfully.')
            return render(request,"addquestion.html",{'add':add})
        else:
            messages.error(request, 'Failed Add. Please Add Question Again.')
    else:
        form = FormDiscussion(None)
    return render(request, 'addquestion.html', { 'form' : form })

def editquestion(request):
    if request.method == 'POST':
        form = FormDiscussion(request.POST)
        if form.is_valid():
            form.save()
            question = request.POST.get('question')
            description = request.POST.get('description')
            file = request.POST.get('file')
            edit = editquestion(question=question,description=description,file=file)
            edit.save()
            messages.success(request, 'Question Edited Successfully.')
            return render(request,"editquestion.html",{'edit':edit})
        else:
            messages.error(request, 'Failed Edit. Please Edit Question Again.')
    else:
        form = FormDiscussion(None)
    return render(request, 'editquestion.html', { 'form' : form })

def replyquestion(request):
    if request.method == 'POST':
        form = FormDiscussioncomment(request.POST)
        if form.is_valid():
            form.save()
            comment = request.POST.get('comment')
            file = request.POST.get('file')
            add = replyquestion(comment=comment,file=file)
            add.save()
            messages.success(request, 'Question Replied Successfully.')
            return render(request,"replyquestion.html",{'add':add})
        else:
            messages.error(request, 'Failed Reply. Please Reply Question Again.')
    else:
        form = FormDiscussioncomment(None)
    return render(request, 'replyquestion.html', { 'form' : form })

def editcomment(request):
    if request.method == 'POST':
        form = FormDiscussioncomment(request.POST)
        if form.is_valid():
            form.save()
            comment = request.POST.get('comment')
            file = request.POST.get('file')
            edit = editcomment(comment=comment,file=file)
            edit.save()
            messages.success(request, 'Comment Edited Successfully.')
            return render(request,"editcomment.html",{'edit':edit})
        else:
            messages.error(request, 'Failed Edit. Please Edit Comment Again.')
    else:
        form = FormDiscussioncomment(None)
    return render(request, 'editcomment.html', { 'form' : form })

def grades(request):
    return render(request, "grades.html")

def checkanswer(request):
    if request.method == 'POST':
        form = FormQuestionselection(request.POST)
        selection = request.POST.get('selection')
        answer = request.POST.get('answer')
        add = checkanswer(selection=selection,answer=answer)
        add.save()
        return render(request,"checkanswer.html",{'add':add})
    else:
        form = FormQuestionselection(None)
    return render(request, 'checkanswer.html', { 'form' : form })

def admingrades(request):
    return render(request, "admingrades.html")

def quizzes(request):
    return render(request, "quizzes.html")

def attendquiz(request):
    if request.method == 'POST':
        form = FormQuizquestion(request.POST)
        question = request.POST.get('question')
        marks = request.POST.get('marks')
        add = attendquiz(question=question,marks=marks)
        add.save()
        return render(request,"attendquiz.html",{'add':add})
    else:
        form = FormQuizquestion(None)
    return render(request, 'attendquiz.html', { 'form' : form })

def adminquizzes(request):
    return render(request, "adminquizzes.html")

def addquiz(request):
    if request.method == 'POST':
        form = FormQuiz(request.POST)
        title = request.POST.get('title')
        duration = request.POST.get('duration')
        attempt = request.POST.get('attempt')
        add = addquiz(title=title,duration=duration,attempt=attempt)
        add.save()
        return render(request,"addquiz.html",{'add':add})
    else:
        form = FormQuiz(None)
    return render(request, 'addquiz.html', { 'form' : form })

def addquizquestion(request):
    if request.method == 'POST':
        form = FormQuizquestion(request.POST)
        if form.is_valid():
            form.save()
            question = request.POST.get('question')
            marks = request.POST.get('marks')
            add = addquizquestion(question=question,marks=marks)
            add.save()
            messages.success('Quiz Question added successfully!')
            return render(request,"addquizquestion.html",{'add':add})
    else:
        form = FormQuizquestion(None)
    return render(request, 'addquizquestion.html', { 'form' : form })

def editquiz(request):
    if request.method == 'POST':
        form = FormQuiz(request.POST)
        title = request.POST.get('title')
        duration = request.POST.get('duration')
        attempt = request.POST.get('attempt')
        add = editquiz(title=title,duration=duration,attempt=attempt)
        add.save()
        return render(request,"editquiz.html",{'add':add})
    else:
        form = FormQuiz(None)
    return render(request, 'editquiz.html', { 'form' : form })

def editquizquestion(request):
    if request.method == 'POST':
        form = FormQuizquestion(request.POST)
        question = request.POST.get('question')
        marks = request.POST.get('marks')
        add = editquizquestion(question=question,marks=marks)
        add.save()
        return render(request,"editquizquestion.html",{'add':add})
    else:
        form = FormQuizquestion(None)
    return render(request, 'editquizquestion.html', { 'form' : form })

def deletequiz(request):
    if request.method == 'POST':
        form = FormQuizquestion(request.POST)
        question = request.POST.get('question')
        marks = request.POST.get('marks')
        add = deletequiz(question=question,marks=marks)
        add.save()
        return render(request,"deletequiz.html",{'add':add})
    else:
        form = FormQuizquestion(None)
    return render(request, 'deletequiz.html', { 'form' : form })

def show_pdf(request):
    filepath = os.path.join('static', 'sample.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')