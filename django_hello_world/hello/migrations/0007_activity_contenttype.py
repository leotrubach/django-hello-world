# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Activity.modelname'
        db.delete_column('hello_activity', 'modelname')

        # Deleting field 'Activity.appname'
        db.delete_column('hello_activity', 'appname')

        # Deleting field 'Activity.object_pk'
        db.delete_column('hello_activity', 'object_pk')

        # Adding field 'Activity.content_type'
        db.add_column('hello_activity', 'content_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['contenttypes.ContentType']),
                      keep_default=False)

        # Adding field 'Activity.object_id'
        db.add_column('hello_activity', 'object_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Activity.modelname'
        raise RuntimeError("Cannot reverse this migration. 'Activity.modelname' and its values cannot be restored.")


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'hello.activity': {
            'Meta': {'object_name': 'Activity'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_logged': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
            'path': ('django.db.models.fields.TextField', [], {}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['hello']
