from django.core.mail import send_mail
from django.db import connection
from django.shortcuts import render, redirect
from onlinetutorapp.models import Coursematerial, Coursesubject, Discussion, Discussioncomment, Helpdesk, Homepage, Quiz, Todolist, User, Userrole, Role, Quizquestion
from .forms import FormAddMaterial, FormForgotPassword, FormHelpdesk, FormTodolist, FormUser, FormUserLogin, FormAddQuestion, FormReplyQuestion, FormQuestionselection, FormAddQuiz, FormQuizquestion
from django.contrib import messages
from django.contrib.postgres.search import *

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
    todolists = get_popup_todolist(userid)
    context = {'userid' : userid, 'currenttitle' : info.title, 'file1url' : info.file1, 'file2url' : info.file2, 'roleid' : userrole.roleid_id, 'todolists': todolists}
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
            form.save()
            fullname = form.cleaned_data.get('name')
            staffid = form.cleaned_data.get('staffid')
            get_email_pass(staffid)
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
        todolist = Todolist.objects.all().filter(userid = userid, isactive = 1)
        context = {'userid' : userid, 'todolist' : todolist}
        return context
    except Todolist.DoesNotExist:
        return None

def get_popup_todolist(userid):
    try:
        todolist = Todolist.objects.all().filter(userid = userid, isactive = 1, status = 0).order_by('timeend')
        if todolist: 
            msg=""
            for todo in todolist:
                msg = msg+todo.task+"\n"
            return {'todolists':msg}
        return None
    except Todolist.DoesNotExist:
        return False

#status changes in checkbox
def checkbox(request, userid):
    id=request.POST.get('id')
    if request.POST.get('checkbox') == '1':
        Todolist.objects.filter(id=id, userid = User.objects.get(id=userid)).update(status = 0)
    else:
        Todolist.objects.filter(id=id, userid = User.objects.get(id=userid)).update(status = 1)

def todolist(request, userid):
    if request.method == 'POST':
        #deletetask
        if request.POST.get('delete'):
            deletetask(request, userid)
            messages.success(request, "Task deleted.")
        #edit task status
        elif request.POST.get('checkbox'):
            checkbox(request, userid)
            messages.success(request, "Task status updated.")      
        #add task
        elif(request.POST.get('task') != '' and request.POST.get('timeend')!= ''):
            newtask = Todolist.objects.create(userid = User.objects.get(id = userid), task = request.POST.get('task'), timeend = request.POST.get('timeend'))
            newtask.save()
            messages.success(request, "Task added.")
        else:
            messages.error(request, 'Your information is invalid. Please try again.')
    #get tasks
    context = getinfotodolist(userid)
    #show tasks
    form = FormTodolist(None)
    context['form'] = form
    return render(request, 'todolist.html', context)

def deletetask(request, userid):
    id=request.POST.get('id')
    Todolist.objects.filter(id=id, userid = User.objects.get(id=userid)).update(isactive = 0)
    
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
    try:
        coursemateriallist = Coursematerial.objects.all().filter(isactive = 1).order_by("coursetopic")
        for coursematerial in coursemateriallist:
            coursematerial.file_url = coursematerial.file.url.replace("onlinetutorapp/static/", "")
        return coursemateriallist
    except Coursematerial.DoesNotExist:
        return None

def getcoursepageinfo(request, userid):
    materialinfo = getcoursematerialinfo()
    info = {'materialinfo' : materialinfo, 'userid' : userid}
    return (request, info)

def coursepage(request, userid):
    userrole = get_userrole(userid)
    list = getcoursematerialinfo()
    context = {'userid' : userid, 'roleid' : userrole.roleid_id, 'list' : list}
    if request.method == 'POST':
        if request.POST.get('delete'):
            return redirect(request, "deletematerials.html", userid)
        elif request.POST.get('add'):
            return redirect(request, "addmaterials.html", userid)
    else:
        return render(request, "coursepage.html", context)

def addmaterials(request, userid):
    context = {'userid':userid}
    if request.method == 'POST':
        form = FormAddMaterial(request.POST)
        if form.is_valid():
            newmaterials = Coursematerial.objects.create(title = request.POST.get('title'), description = request.POST.get('description'), file = request.FILES.get('myfile'), coursetopic = request.POST.get('coursetopic'))
            newmaterials.save()
            messages.success(request, 'Subject materials added successfully.')
        else:
            messages.error(request, 'Your information is invalid. Please try again.')
        return render(request, "addmaterials.html", context)
    else:
        form = FormAddMaterial(None)
        return render(request, 'addmaterials.html', context)

def deletematerials(request, userid):
    if request.method == 'POST':
        title = request.POST.get('title')
        findid = Coursematerial.objects.get(title = title)
        Coursematerial.objects.filter(id=findid.id).update(isactive = 0)
        messages.success(request, "Material deleted.")
    material = Coursematerial.objects.raw('SELECT * FROM coursematerial WHERE isactive=1')
    context = {'material' : material, 'userid': userid}
    return render(request, 'deletematerials.html', context)

'''def getdiscussionboardinfo(userid):
    #Lau Wan Jing: https://stackoverflow.com/a/61908629 -- fetch all data from disucssion table
    cursor = connection.cursor()
    query = "Select * from discussion WHERE isactive=1"
    cursor.execute(query)
    list = [list for list in cursor.fetchall()]
    list = [(list), userid]
    return list'''

#Lau Wan Jing: get question data
def getdiscussioninfo(userid):
    try:
        discussion = Discussion.objects.all().filter(isactive = 1)
        context = {'userid' : userid, 'discussion' : discussion}
        return context
    except Discussion.DoesNotExist:
        return None

def discussionboard(request, userid):
    discuss = getdiscussioninfo(userid)
    if request.method == 'POST':
        if request.POST.get('search'):
            return redirect(request, "searchquestion.html", userid)
        elif request.POST.get('add'):
            return redirect(request, "addquestion.html", userid)
        elif request.POST.get('deletequestion'):
            return redirect(request, "deletequestion.html", userid)
        elif request.POST.get('deletecomment'):
            return redirect(request, "deletecomment.html", userid)
        elif request.POST.get('view'):
            questionid = request.POST.get('value')
            context = {'userid' : userid, 'questionid' : questionid}
            discussionquestion(request, context)
            return redirect(request, "discussionquestion.html", context)
    else:
        return render(request, "discussionboard.html", discuss)
    
def addquestion(request, userid):
    context = {'userid':userid}
    if request.method == 'POST':
        form = FormAddQuestion(request.POST)
        if form.is_valid():
            addquestion = Discussion.objects.create(userid = User.objects.get(id=userid), question = request.POST.get('question'), description = request.POST.get('description'))
            addquestion.save()
            messages.success(request, 'Question added successfully.')
            return redirect(request, "addquestion.html")
        else:
            messages.error(request, 'Your information is invalid. Please try again.')
        return render(request, "addquestion.html")
    else:
        form = FormAddQuestion(None)
        return render(request, 'addquestion.html', context)

#Lau Wan Jing: https://docs.djangoproject.com/en/4.0/ref/contrib/postgres/search/ -- search question
def searchquestion(request, userid):
    if request.method == 'POST':
        word = request.POST.get('word')
        result = Discussion.objects.filter(body_text__search=word)
        context = {'userid' : userid, 'result' : result}
        return render(request, "searchquestion.html", context)
    else:
        messages.error(request, 'Result not found.')
        return render(request, "searchquestion.html", userid)

def getdiscussionquestioninfo(context):
    try:
        question = Discussion.objects.all().filter(id=context.questionid)
        context['question'] = question
        return context
    except Discussion.DoesNotExist:
        return None

def deletequestion(request, userid):
    if request.method == 'POST':
        question = request.POST.get('question')
        findid = Discussion.objects.get(question = question)
        Discussion.objects.filter(id=findid.id).update(isactive = 0)
        messages.success(request, "Question deleted.")
    question = Discussion.objects.raw('SELECT * FROM discussion WHERE isactive=1')
    context = {'question' : question, 'userid': userid}
    return render(request, 'deletematerials.html', context)

def deletecomment(request, userid):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        findid = Discussioncomment.objects.get(comment = comment)
        Discussioncomment.objects.filter(id=findid.id).update(isactive = 0)
        messages.success(request, "Comment deleted.")
        Discussion.objects.filter(title=request.POST.get('deletecomment').update(isactive = 0))
    comment = Discussioncomment.objects.raw('SELECT * FROM discussioncomment WHERE isactive=1')
    context = {'comment' : comment, 'userid': userid}
    return render(request, 'deletematerials.html', context)

def discussionquestion(request, context):
    question = getdiscussionquestioninfo(context)
    context = {'question': question}
    if request.method == 'POST':
        if request.POST.get('reply'):
            replyquestion(request, context)
            return redirect(request, "replycomment.html", context)
    else:
        return render(request, "discussionquestion.html", context)

def replyquestion(request, context):
    context = {'context':context}
    if request.method == 'POST':
        form = FormReplyQuestion(request.POST)
        if form.is_valid():
            replyquestion = Discussioncomment.objects.create(discussionid = Discussion.objects.get(id=context.questionid), comment = request.POST.get('comment'))
            replyquestion.save()
            messages.success(request, 'Question replied successfully.')
            return render(request, "replyquestion.html", context)
        else:
            messages.error(request, 'Your information is invalid. Please try again.')
        return render(request, "replyquestion.html", context)
    else:
        form = FormReplyQuestion(None)
        return render(request, 'replyquestion.html', context)

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

def getquizzesinfo(userid):
    cursor = connection.cursor()
    query = "Select * from quiz WHERE isactive=1"
    cursor.execute(query)
    list = [list for list in cursor.fetchall()]
    list = [(list), userid]
    return list

#add userid find user name function

def quizzes(request, userid):
    quiz = getquizzesinfo(userid)
    quiz['userid'] = userid
    return render(request, "quizzes.html", quiz)

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

#def adminquizzes(request):
    #return render(request, "adminquizzes.html")

def addquiz(request, quizid):
    if request.method == 'POST':
        form = FormAddQuiz(request.POST)
        if form.is_valid():
            addquiz = Quiz.objects.create(quizid = Quiz.objects.get(id=quizid), title = request.POST.get('title'), duration = request.POST.get('duration'), attempt = request.POST.get('attempt'))
            addquiz.save()
            messages.success(request, 'Quiz added successfully.')
            return redirect(request, "addquiz.html")
        else:
            messages.error(request, 'Your information is invalid. Please try again.')
        return render(request, "addquiz.html")
    else:
        form = FormAddQuiz(None)
        return render(request, 'addquiz.html')

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

def deletequiz(request, userid):
    id=request.POST.get('id')
    Quizquestion.objects.filter(id=id, userid = User.objects.get(id=userid)).update(isactive = 0)