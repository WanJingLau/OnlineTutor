# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import random
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CaptchaCaptchastore(models.Model):
    id = models.BigAutoField(primary_key=True)
    challenge = models.CharField(max_length=32)
    response = models.CharField(max_length=32)
    hashkey = models.CharField(unique=True, max_length=40)
    expiration = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'captcha_captchastore'


class Coursematerial(models.Model):
    coursetopicid = models.ForeignKey('Coursetopic', models.DO_NOTHING, db_column='coursetopicid')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    file = models.TextField()
    isactive = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coursematerial'


class Coursesubject(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid')
    name = models.CharField(max_length=255)
    isactive = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coursesubject'


class Coursetopic(models.Model):
    id = models.OneToOneField(Coursesubject, models.DO_NOTHING, db_column='id', primary_key=True)
    coursesubject = models.IntegerField()
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    isactive = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coursetopic'


class Discussion(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid')
    coursetopicid = models.ForeignKey(Coursetopic, models.DO_NOTHING, db_column='coursetopicid')
    question = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    file1 = models.TextField(blank=True, null=True)
    isactive = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discussion'


class Discussioncomment(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid')
    discussionid = models.ForeignKey(Discussion, models.DO_NOTHING, db_column='discussionid')
    comment = models.CharField(max_length=255)
    file1 = models.TextField(blank=True, null=True)
    isactive = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discussioncomment'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Helpdesk(models.Model):
    question = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'helpdesk'


class Homepage(models.Model):
    title = models.CharField(max_length=255)
    file1 = models.TextField()
    file2 = models.TextField()

    class Meta:
        managed = False
        db_table = 'homepage'


class PostOfficeAttachment(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255)
    headers = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_office_attachment'


class PostOfficeAttachmentEmails(models.Model):
    id = models.BigAutoField(primary_key=True)
    attachment = models.ForeignKey(PostOfficeAttachment, models.DO_NOTHING)
    email = models.ForeignKey('PostOfficeEmail', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'post_office_attachment_emails'
        unique_together = (('attachment', 'email'),)


class PostOfficeEmail(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_email = models.CharField(max_length=254)
    to = models.TextField()
    cc = models.TextField()
    bcc = models.TextField()
    subject = models.CharField(max_length=989)
    message = models.TextField()
    html_message = models.TextField()
    status = models.PositiveSmallIntegerField(blank=True, null=True)
    priority = models.PositiveSmallIntegerField(blank=True, null=True)
    created = models.DateTimeField()
    last_updated = models.DateTimeField()
    scheduled_time = models.DateTimeField(blank=True, null=True)
    headers = models.TextField(blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    template = models.ForeignKey('PostOfficeEmailtemplate', models.DO_NOTHING, blank=True, null=True)
    backend_alias = models.CharField(max_length=64)
    number_of_retries = models.PositiveIntegerField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    message_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_office_email'


class PostOfficeEmailtemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.CharField(max_length=255)
    content = models.TextField()
    html_content = models.TextField()
    created = models.DateTimeField()
    last_updated = models.DateTimeField()
    default_template = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    language = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'post_office_emailtemplate'
        unique_together = (('name', 'language', 'default_template'),)


class PostOfficeLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField()
    status = models.PositiveSmallIntegerField()
    exception_type = models.CharField(max_length=255)
    message = models.TextField()
    email = models.ForeignKey(PostOfficeEmail, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'post_office_log'


class Questionselection(models.Model):
    quizquestionid = models.ForeignKey('Quizquestion', models.DO_NOTHING, db_column='quizquestionid')
    selection = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    isactive = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questionselection'


class Quiz(models.Model):
    coursetopicid = models.ForeignKey(Coursetopic, models.DO_NOTHING, db_column='coursetopicid')
    title = models.CharField(max_length=100)
    duration = models.TimeField()
    attempt = models.IntegerField()
    isactive = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quiz'


class Quizquestion(models.Model):
    quizid = models.ForeignKey(Quiz, models.DO_NOTHING, db_column='quizid')
    question = models.CharField(max_length=255)
    marks = models.IntegerField()
    isactive = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quizquestion'


class Role(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'role'


class Todolist(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid')
    task = models.CharField(max_length=50)
    timeend = models.DateTimeField()
    status = models.IntegerField(default=1)
    isactive = models.IntegerField(blank=True, null=True, default=1)

    class Meta:
        managed = False
        db_table = 'todolist'


class User(models.Model):
    staffid = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    # Lau Wan Jing: https://stackoverflow.com/questions/755857/default-value-for-field-in-django-model
    digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    passw = ""
    for i in range(0, 8):
        passw = passw + random.choice(digits)
    x = passw
    password = models.CharField(max_length=100, default=x)
    isactive = models.IntegerField(blank=True, null=True, default=1)

    class Meta:
        managed = False
        db_table = 'user'


class Userquizselection(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid')
    questionselectionid = models.ForeignKey(Questionselection, models.DO_NOTHING, db_column='questionselectionid')
    answercorrect = models.IntegerField()
    attemptcount = models.IntegerField()
    score = models.IntegerField()
    isactive = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userquizselection'


class Userrole(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid')
    roleid = models.ForeignKey(Role, models.DO_NOTHING, db_column='roleid')

    class Meta:
        managed = False
        db_table = 'userrole'
