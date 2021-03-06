# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Job'
        db.create_table('ganeti_web_job', (
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('job_id', self.gf('django.db.models.fields.IntegerField')()),
            ('cluster_hash', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('cached', self.gf('utils.fields.PreciseDateTimeField')(null=True, max_digits=18, decimal_places=6)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jobs', to=orm['ganeti_web.Cluster'])),
            ('finished', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('ignore_cache', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('mtime', self.gf('utils.fields.PreciseDateTimeField')(null=True, max_digits=18, decimal_places=6)),
            ('serialized_info', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('cleared', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ganeti_web', ['Job'])

        # Adding model 'VirtualMachine'
        db.create_table('ganeti_web_virtualmachine', (
            ('status', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('ram', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('disk_size', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('cluster_hash', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('cached', self.gf('utils.fields.PreciseDateTimeField')(null=True, max_digits=18, decimal_places=6)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('secondary_node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='secondary_vms', null=True, to=orm['ganeti_web.Node'])),
            ('primary_node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primary_vms', null=True, to=orm['ganeti_web.Node'])),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='virtual_machines', to=orm['ganeti_web.Cluster'])),
            ('operating_system', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ganeti_web.Job'], null=True)),
            ('ignore_cache', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ganeti_web.VirtualMachineTemplate'], null=True)),
            ('mtime', self.gf('utils.fields.PreciseDateTimeField')(null=True, max_digits=18, decimal_places=6)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='virtual_machines', null=True, to=orm['ganeti_web.ClusterUser'])),
            ('virtual_cpus', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('serialized_info', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('pending_delete', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ganeti_web', ['VirtualMachine'])

        # Adding unique constraint on 'VirtualMachine', fields ['cluster', 'hostname']
        db.create_unique('ganeti_web_virtualmachine', ['cluster_id', 'hostname'])

        # Adding model 'Node'
        db.create_table('ganeti_web_node', (
            ('cluster_hash', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('cached', self.gf('utils.fields.PreciseDateTimeField')(null=True, max_digits=18, decimal_places=6)),
            ('hostname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['ganeti_web.Cluster'])),
            ('disk_total', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('disk_free', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ignore_cache', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('ram_total', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('ram_free', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('mtime', self.gf('utils.fields.PreciseDateTimeField')(null=True, max_digits=18, decimal_places=6)),
            ('offline', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('serialized_info', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('last_job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ganeti_web.Job'], null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ganeti_web', ['Node'])

        # Adding model 'Cluster'
        db.create_table('ganeti_web_cluster', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('disk', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('cached', self.gf('utils.fields.PreciseDateTimeField')(null=True, max_digits=18, decimal_places=6)),
            ('hostname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('ram', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(default=5080)),
            ('last_job', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cluster_last_job', null=True, to=orm['ganeti_web.Job'])),
            ('ignore_cache', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('mtime', self.gf('utils.fields.PreciseDateTimeField')(null=True, max_digits=18, decimal_places=6)),
            ('virtual_cpus', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('serialized_info', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ganeti_web', ['Cluster'])

        # Adding model 'VirtualMachineTemplate'
        db.create_table('ganeti_web_virtualmachinetemplate', (
            ('nic_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('nic_mode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ganeti_web.Cluster'], null=True)),
            ('disk_template', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pnode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('cdrom_image_path', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('name_check', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('start', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('memory', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('kernel_path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('boot_order', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('serial_console', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('snode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('disk_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('iallocator_hostname', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('disk_size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('nic_link', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('root_path', self.gf('django.db.models.fields.CharField')(default='/', max_length=255, null=True, blank=True)),
            ('vcpus', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('iallocator', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('ganeti_web', ['VirtualMachineTemplate'])

        # Adding model 'TestModel'
        db.create_table('ganeti_web_testmodel', (
            ('cached', self.gf('utils.fields.PreciseDateTimeField')(null=True, max_digits=18, decimal_places=6)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ganeti_web.Cluster'])),
            ('ignore_cache', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('mtime', self.gf('utils.fields.PreciseDateTimeField')(null=True, max_digits=18, decimal_places=6)),
            ('serialized_info', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ganeti_web', ['TestModel'])

        # Adding model 'GanetiError'
        db.create_table('ganeti_web_ganetierror', (
            ('obj_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ganeti_errors', to=orm['contenttypes.ContentType'])),
            ('code', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('obj_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ganeti_web.Cluster'])),
            ('msg', self.gf('django.db.models.fields.TextField')()),
            ('cleared', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ganeti_web', ['GanetiError'])

        # Adding model 'ClusterUser'
        db.create_table('ganeti_web_clusteruser', (
            ('real_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('ganeti_web', ['ClusterUser'])

        # Adding model 'Profile'
        db.create_table('ganeti_web_profile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('clusteruser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ganeti_web.ClusterUser'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('ganeti_web', ['Profile'])

        # Adding model 'Organization'
        db.create_table('ganeti_web_organization', (
            ('group', self.gf('django.db.models.fields.related.OneToOneField')(related_name='organization', unique=True, to=orm['auth.Group'])),
            ('clusteruser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ganeti_web.ClusterUser'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('ganeti_web', ['Organization'])

        # Adding model 'Quota'
        db.create_table('ganeti_web_quota', (
            ('ram', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='quotas', to=orm['ganeti_web.Cluster'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='quotas', to=orm['ganeti_web.ClusterUser'])),
            ('virtual_cpus', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('disk', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ganeti_web', ['Quota'])

        # Adding model 'SSHKey'
        db.create_table('ganeti_web_sshkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ssh_keys', to=orm['auth.User'])),
        ))
        db.send_create_signal('ganeti_web', ['SSHKey'])

        # Adding model 'Cluster_Perms'
        db.create_table('ganeti_web_cluster_perms', (
            ('obj', self.gf('django.db.models.fields.related.ForeignKey')(related_name='operms', to=orm['ganeti_web.Cluster'])),
            ('tags', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('admin', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('replace_disks', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('create_vm', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('migrate', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('export', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Cluster_uperms', null=True, to=orm['auth.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Cluster_gperms', null=True, to=orm['auth.Group'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ganeti_web', ['Cluster_Perms'])

        # Adding model 'VirtualMachine_Perms'
        db.create_table('ganeti_web_virtualmachine_perms', (
            ('obj', self.gf('django.db.models.fields.related.ForeignKey')(related_name='operms', to=orm['ganeti_web.VirtualMachine'])),
            ('power', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('tags', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('admin', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('modify', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('remove', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='VirtualMachine_uperms', null=True, to=orm['auth.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='VirtualMachine_gperms', null=True, to=orm['auth.Group'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ganeti_web', ['VirtualMachine_Perms'])


    def backwards(self, orm):

        # Deleting model 'Job'
        db.delete_table('ganeti_web_job')

        # Deleting model 'VirtualMachine'
        db.delete_table('ganeti_web_virtualmachine')

        # Removing unique constraint on 'VirtualMachine', fields ['cluster', 'hostname']
        db.delete_unique('ganeti_web_virtualmachine', ['cluster_id', 'hostname'])

        # Deleting model 'Node'
        db.delete_table('ganeti_web_node')

        # Deleting model 'Cluster'
        db.delete_table('ganeti_web_cluster')

        # Deleting model 'VirtualMachineTemplate'
        db.delete_table('ganeti_web_virtualmachinetemplate')

        # Deleting model 'TestModel'
        db.delete_table('ganeti_web_testmodel')

        # Deleting model 'GanetiError'
        db.delete_table('ganeti_web_ganetierror')

        # Deleting model 'ClusterUser'
        db.delete_table('ganeti_web_clusteruser')

        # Deleting model 'Profile'
        db.delete_table('ganeti_web_profile')

        # Deleting model 'Organization'
        db.delete_table('ganeti_web_organization')

        # Deleting model 'Quota'
        db.delete_table('ganeti_web_quota')

        # Deleting model 'SSHKey'
        db.delete_table('ganeti_web_sshkey')

        # Deleting model 'Cluster_Perms'
        db.delete_table('ganeti_web_cluster_perms')

        # Deleting model 'VirtualMachine_Perms'
        db.delete_table('ganeti_web_virtualmachine_perms')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ganeti_web.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'cached': ('utils.fields.PreciseDateTimeField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '6'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'disk': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_cache': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_job': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cluster_last_job'", 'null': 'True', 'to': "orm['ganeti_web.Job']"}),
            'mtime': ('utils.fields.PreciseDateTimeField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '6'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5080'}),
            'ram': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'serialized_info': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'virtual_cpus': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ganeti_web.cluster_perms': {
            'Meta': {'object_name': 'Cluster_Perms'},
            'admin': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'create_vm': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'export': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Cluster_gperms'", 'null': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'migrate': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'obj': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'operms'", 'to': "orm['ganeti_web.Cluster']"}),
            'replace_disks': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'tags': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Cluster_uperms'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'ganeti_web.clusteruser': {
            'Meta': {'object_name': 'ClusterUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'})
        },
        'ganeti_web.ganetierror': {
            'Meta': {'object_name': 'GanetiError'},
            'cleared': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ganeti_web.Cluster']"}),
            'code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.TextField', [], {}),
            'obj_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'obj_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ganeti_errors'", 'to': "orm['contenttypes.ContentType']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'ganeti_web.job': {
            'Meta': {'object_name': 'Job'},
            'cached': ('utils.fields.PreciseDateTimeField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '6'}),
            'cleared': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'to': "orm['ganeti_web.Cluster']"}),
            'cluster_hash': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'finished': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_cache': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'job_id': ('django.db.models.fields.IntegerField', [], {}),
            'mtime': ('utils.fields.PreciseDateTimeField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '6'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'serialized_info': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'ganeti_web.node': {
            'Meta': {'object_name': 'Node'},
            'cached': ('utils.fields.PreciseDateTimeField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '6'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': "orm['ganeti_web.Cluster']"}),
            'cluster_hash': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'disk_total': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_cache': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ganeti_web.Job']", 'null': 'True'}),
            'mtime': ('utils.fields.PreciseDateTimeField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '6'}),
            'offline': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'ram_total': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'serialized_info': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'})
        },
        'ganeti_web.organization': {
            'Meta': {'object_name': 'Organization', '_ormbases': ['ganeti_web.ClusterUser']},
            'clusteruser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ganeti_web.ClusterUser']", 'unique': 'True', 'primary_key': 'True'}),
            'group': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'organization'", 'unique': 'True', 'to': "orm['auth.Group']"})
        },
        'ganeti_web.profile': {
            'Meta': {'object_name': 'Profile', '_ormbases': ['ganeti_web.ClusterUser']},
            'clusteruser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ganeti_web.ClusterUser']", 'unique': 'True', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'ganeti_web.quota': {
            'Meta': {'object_name': 'Quota'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quotas'", 'to': "orm['ganeti_web.Cluster']"}),
            'disk': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ram': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quotas'", 'to': "orm['ganeti_web.ClusterUser']"}),
            'virtual_cpus': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        'ganeti_web.sshkey': {
            'Meta': {'object_name': 'SSHKey'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ssh_keys'", 'to': "orm['auth.User']"})
        },
        'ganeti_web.testmodel': {
            'Meta': {'object_name': 'TestModel'},
            'cached': ('utils.fields.PreciseDateTimeField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '6'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ganeti_web.Cluster']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_cache': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'mtime': ('utils.fields.PreciseDateTimeField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '6'}),
            'serialized_info': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'})
        },
        'ganeti_web.virtualmachine': {
            'Meta': {'unique_together': "(('cluster', 'hostname'),)", 'object_name': 'VirtualMachine'},
            'cached': ('utils.fields.PreciseDateTimeField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '6'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'virtual_machines'", 'to': "orm['ganeti_web.Cluster']"}),
            'cluster_hash': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'disk_size': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_cache': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ganeti_web.Job']", 'null': 'True'}),
            'mtime': ('utils.fields.PreciseDateTimeField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '6'}),
            'operating_system': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'virtual_machines'", 'null': 'True', 'to': "orm['ganeti_web.ClusterUser']"}),
            'pending_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'primary_node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_vms'", 'null': 'True', 'to': "orm['ganeti_web.Node']"}),
            'ram': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'secondary_node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secondary_vms'", 'null': 'True', 'to': "orm['ganeti_web.Node']"}),
            'serialized_info': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ganeti_web.VirtualMachineTemplate']", 'null': 'True'}),
            'virtual_cpus': ('django.db.models.fields.IntegerField', [], {'default': '-1'})
        },
        'ganeti_web.virtualmachine_perms': {
            'Meta': {'object_name': 'VirtualMachine_Perms'},
            'admin': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'VirtualMachine_gperms'", 'null': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'obj': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'operms'", 'to': "orm['ganeti_web.VirtualMachine']"}),
            'power': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'remove': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'tags': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'VirtualMachine_uperms'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'ganeti_web.virtualmachinetemplate': {
            'Meta': {'object_name': 'VirtualMachineTemplate'},
            'boot_order': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cdrom_image_path': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ganeti_web.Cluster']", 'null': 'True'}),
            'disk_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'disk_template': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'disk_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'iallocator': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'iallocator_hostname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kernel_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'memory': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name_check': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'nic_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nic_mode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nic_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pnode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'root_path': ('django.db.models.fields.CharField', [], {'default': "'/'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'serial_console': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'snode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'vcpus': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ganeti_web']
