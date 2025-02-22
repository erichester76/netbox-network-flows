from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('virtualization', '0001_initial'),  # Adjust based on your NetBox version
    ]
    operations = [
        migrations.CreateModel(
            name='TrafficFlow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('src_ip', models.CharField(max_length=45)),
                ('dst_ip', models.CharField(max_length=45)),
                ('protocol', models.CharField(max_length=10)),
                ('src_port', models.IntegerField()),
                ('dst_port', models.IntegerField()),
                ('server_id', models.CharField(max_length=100)),
                ('timestamp', models.FloatField()),
                ('virtual_machine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='traffic_flows', to='virtualization.virtualmachine')),
            ],
            options={
                'unique_together': {('src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'server_id')},
            },
        ),
    ]