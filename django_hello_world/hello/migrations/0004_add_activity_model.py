# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Activity'
        db.create_table('hello_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('operation', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('date_logged', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('appname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('modelname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('hello', ['Activity'])

    def backwards(self, orm):
        # Deleting model 'Activity'
        db.delete_table('hello_activity')


    models = {
        'hello.activity': {
            'Meta': {'object_name': 'Activity'},
            'appname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date_logged': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modelname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'hello.owner': {
            'Meta': {'object_name': 'Owner'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'other': ('django.db.models.fields.TextField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'hello.request': {
            'Meta': {'object_name': 'Request'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logged_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'path': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['hello']