from django.db import models


class Owner(models.Model):
    firstname = models.CharField(max_length=25, verbose_name='first name')
    lastname = models.CharField(max_length=25, verbose_name='last name')
    birthday = models.DateField(verbose_name='birthday')
    bio = models.TextField(verbose_name='bio')
    email = models.EmailField(verbose_name='email')
    jabber = models.CharField(max_length=25, verbose_name='jabber')
    skype = models.CharField(max_length=25, verbose_name='skype')
    other = models.TextField(verbose_name='other information')
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
    dt_request = models.DateTimeField(auto_now_add=True, verbose_name='request time')

    def __unicode__(self):
        return '%(dt_request)s %(method)s %(path)s' % {'dt_request': self.dt_request,
                                                       'path': self.path,
                                                       'method': self.method}

    class Meta:
        verbose_name = 'request'
        verbose_name_plural = 'requests'
