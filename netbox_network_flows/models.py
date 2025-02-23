from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from netbox.models import NetBoxModel
from ipam.models import IPAddress
from virtualization.models import VirtualMachine
from dcim.models import Device


class TrafficFlow(NetBoxModel):
    src_ip = models.CharField(max_length=45)
    dst_ip = models.CharField(max_length=45)
    protocol = models.CharField(max_length=10)
    service_port = models.IntegerField()
    server_id = models.CharField(max_length=100)
    src_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='src_traffic_flows', null=True, blank=True)
    src_object_id = models.PositiveIntegerField(null=True, blank=True)
    src_object = GenericForeignKey('src_content_type', 'src_object_id')
    dst_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='dst_traffic_flows', null=True, blank=True)
    dst_object_id = models.PositiveIntegerField(null=True, blank=True)
    dst_object = GenericForeignKey('dst_content_type', 'dst_object_id')
    timestamp = models.FloatField()

    class Meta:
        unique_together = ('src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id')

    def save(self, *args, **kwargs):
        if not self.src_content_type or not self.src_object_id:
            try:
                ip = IPAddress.objects.filter(address__contains=self.src_ip).first()
                if ip:
                    if ip.assigned_object:
                        if isinstance(ip.assigned_object, VirtualMachine):
                            self.src_content_type = ContentType.objects.get_for_model(VirtualMachine)
                            self.src_object_id = ip.assigned_object.pk
                        elif isinstance(ip.assigned_object, Device):
                            self.src_content_type = ContentType.objects.get_for_model(Device)
                            self.src_object_id = ip.assigned_object.pk
                    else:
                        self.src_content_type = ContentType.objects.get_for_model(IPAddress)
                        self.src_object_id = ip.pk
            except Exception as e:
                print(f"Error resolving src_ip {self.src_ip}: {str(e)}", exc_info=True)

        # Resolve dst_ip via IPAddress
        if not self.dst_content_type or not self.dst_object_id:
            try:
                ip = IPAddress.objects.filter(address__contains=self.src_ip).first()
                if ip:
                    if ip.assigned_object:
                        if isinstance(ip.assigned_object, VirtualMachine):
                            self.dst_content_type = ContentType.objects.get_for_model(VirtualMachine)
                            self.dst_object_id = ip.assigned_object.pk
                        elif isinstance(ip.assigned_object, Device):
                            self.dst_content_type = ContentType.objects.get_for_model(Device)
                            self.dst_object_id = ip.assigned_object.pk
                    else:
                        self.dst_content_type = ContentType.objects.get_for_model(IPAddress)
                        self.dst_object_id = ip.pk
            except Exception as e:
                print(f"Error resolving dst_ip {self.dst_ip}: {str(e)}", exc_info=True)

        super().save(*args, **kwargs)
        
        if not self.src_content_type or not self.src_object_id:
            try:
                ip = IPAddress.objects.get(address__contains=self.src_ip)
                if ip.assigned_object:
                    if isinstance(ip.assigned_object, VirtualMachine):
                        self.src_content_type = ContentType.objects.get_for_model(VirtualMachine)
                        self.src_object_id = ip.assigned_object.pk
                    elif isinstance(ip.assigned_object, Device):
                        self.src_content_type = ContentType.objects.get_for_model(Device)
                        self.src_object_id = ip.assigned_object.pk
                else:
                    self.src_content_type = ContentType.objects.get_for_model(IPAddress)
                    self.src_object_id = ip.pk
            except IPAddress.DoesNotExist:
                print(f"No IPAddress found for src_ip: {self.src_ip}")

        # Resolve dst_ip via IPAddress
        if not self.dst_content_type or not self.dst_object_id:
            try:
                ip = IPAddress.objects.get(address__contains=self.dst_ip)
                if ip.assigned_object:
                    if isinstance(ip.assigned_object, VirtualMachine):
                        self.dst_content_type = ContentType.objects.get_for_model(VirtualMachine)
                        self.dst_object_id = ip.assigned_object.pk
                    elif isinstance(ip.assigned_object, Device):
                        self.dst_content_type = ContentType.objects.get_for_model(Device)
                        self.dst_object_id = ip.assigned_object.pk
                else:
                    self.dst_content_type = ContentType.objects.get_for_model(IPAddress)
                    self.dst_object_id = ip.pk
            except IPAddress.DoesNotExist:
                print(f"No IPAddress found for dst_ip: {self.dst_ip}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.src_ip} -> {self.dst_ip} ({self.protocol}:{self.service_port})"