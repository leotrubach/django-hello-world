from django.db import models
from django.db.models.signals import post_save, post_delete
from django.db.utils import DatabaseError
from django.dispatch.dispatcher import receiver
from django.core.signals import request_finished
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Owner(models.Model):
    firstname = models.CharField(max_length=25, verbose_name='first name')
    lastname = models.CharField(max_length=25, verbose_name='last name')
    birthday = models.DateField(verbose_name='birthday')
    bio = models.TextField(verbose_name='bio')
    email = models.EmailField(verbose_name='email')
    jabber = models.CharField(max_length=25, verbose_name='jabber')
    skype = models.CharField(max_length=25, verbose_name='skype')
    other = models.TextField(verbose_name='other information')
    photo = models.ImageField(
        upload_to='photos',
        verbose_name='photo', null=True, blank=True)
    active = models.BooleanField(verbose_name='active')

    def __unicode__(self):
        return '%(name)s %(lastname)s' % {'name': self.firstname,
                                          'lastname': self.lastname}

    class Meta:
        verbose_name = 'owner'
        verbose_name_plural = 'owners'


class Request(models.Model):
    method = models.CharField(max_length=10, verbose_name='method')
    path = models.TextField(verbose_name='path')
    logged_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='request time')
    priority = models.IntegerField(default=0, verbose_name='priority')

    def __unicode__(self):
        format_pars = {'logged_date': self.logged_date,
                       'path': self.path,
                       'method': self.method}
        return '%(logged_date)s %(method)s %(path)s' % format_pars

    class Meta:
        verbose_name = 'request'
        verbose_name_plural = 'requests'


class Activity(models.Model):
    operation = models.CharField(
        choices=(('C', 'create'),
                 ('U', 'update'),
                 ('D', 'delete')),
        max_length=10,
        verbose_name='operation')
    date_logged = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=50)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        fmt = '%(date_logged) %(operation)s %(object)s'
        pars = {'date_logged': self.date_logged,
                'operation': self.operation,
                'object': self.content_object}
        return fmt % pars


@receiver(post_save, dispatch_uid="42-test-leo-save")
def on_save(sender, instance=None, created=False, raw=True, **kwargs):
    if raw:
        return
    if issubclass(sender, Activity):
        return
    if created:
        operation = 'C'
    else:
        operation = 'U'
    try:
        Activity(
            operation=operation,
            content_object=instance
        ).save()
    except DatabaseError:
        pass


@receiver(post_delete, dispatch_uid="42-test-leo-delete")
def on_delete(sender, instance=None, **kwargs):
    if not instance:
        return
    if isinstance(sender, Activity):
        return
    Activity(
        operation='D',
        content_object=instance
    ).save()
