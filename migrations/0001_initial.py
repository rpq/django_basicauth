# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('basicauth_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=250)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('basicauth', ['User'])

        # Adding model 'Permission'
        db.create_table('basicauth_permission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('basicauth', ['Permission'])

        # Adding model 'Group'
        db.create_table('basicauth_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('basicauth', ['Group'])

        # Adding model 'UserPermission'
        db.create_table('basicauth_userpermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['basicauth.User'])),
            ('permission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['basicauth.Permission'])),
        ))
        db.send_create_signal('basicauth', ['UserPermission'])

        # Adding unique constraint on 'UserPermission', fields ['user', 'permission']
        db.create_unique('basicauth_userpermission', ['user_id', 'permission_id'])

        # Adding model 'UserGroup'
        db.create_table('basicauth_usergroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['basicauth.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['basicauth.Group'])),
        ))
        db.send_create_signal('basicauth', ['UserGroup'])

        # Adding unique constraint on 'UserGroup', fields ['user', 'group']
        db.create_unique('basicauth_usergroup', ['user_id', 'group_id'])

        # Adding model 'GroupPermission'
        db.create_table('basicauth_grouppermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['basicauth.Group'])),
            ('permission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['basicauth.Permission'])),
        ))
        db.send_create_signal('basicauth', ['GroupPermission'])

        # Adding unique constraint on 'GroupPermission', fields ['group', 'permission']
        db.create_unique('basicauth_grouppermission', ['group_id', 'permission_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'GroupPermission', fields ['group', 'permission']
        db.delete_unique('basicauth_grouppermission', ['group_id', 'permission_id'])

        # Removing unique constraint on 'UserGroup', fields ['user', 'group']
        db.delete_unique('basicauth_usergroup', ['user_id', 'group_id'])

        # Removing unique constraint on 'UserPermission', fields ['user', 'permission']
        db.delete_unique('basicauth_userpermission', ['user_id', 'permission_id'])

        # Deleting model 'User'
        db.delete_table('basicauth_user')

        # Deleting model 'Permission'
        db.delete_table('basicauth_permission')

        # Deleting model 'Group'
        db.delete_table('basicauth_group')

        # Deleting model 'UserPermission'
        db.delete_table('basicauth_userpermission')

        # Deleting model 'UserGroup'
        db.delete_table('basicauth_usergroup')

        # Deleting model 'GroupPermission'
        db.delete_table('basicauth_grouppermission')


    models = {
        'basicauth.group': {
            'Meta': {'object_name': 'Group'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'basicauth.grouppermission': {
            'Meta': {'unique_together': "(('group', 'permission'),)", 'object_name': 'GroupPermission'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['basicauth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['basicauth.Permission']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'basicauth.permission': {
            'Meta': {'object_name': 'Permission'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'basicauth.user': {
            'Meta': {'object_name': 'User'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '250'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'basicauth.usergroup': {
            'Meta': {'unique_together': "(('user', 'group'),)", 'object_name': 'UserGroup'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['basicauth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['basicauth.User']"})
        },
        'basicauth.userpermission': {
            'Meta': {'unique_together': "(('user', 'permission'),)", 'object_name': 'UserPermission'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['basicauth.Permission']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['basicauth.User']"})
        }
    }

    complete_apps = ['basicauth']