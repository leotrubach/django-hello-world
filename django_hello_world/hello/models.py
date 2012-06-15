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