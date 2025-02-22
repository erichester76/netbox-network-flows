from django.db import models
from netbox.models import NetBoxModel
from virtualization.models import VirtualMachine

class TrafficFlow(NetBoxModel):
    src_ip = models.CharField(max_length=45)  # Supports IPv4/IPv6
    dst_ip = models.CharField(max_length=45)
    protocol = models.CharField(max_length=10)
    src_port = models.IntegerField()
    dst_port = models.IntegerField()
    server_id = models.CharField(max_length=100)  # Matches VM name or hostname
    virtual_machine = models.ForeignKey(
        VirtualMachine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='traffic_flows'
    )
    timestamp = models.FloatField()

    class Meta:
        unique_together = ('src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'server_id')

    def save(self, *args, **kwargs):
        # Auto-map to VirtualMachine if server_id matches a VM name
        if not self.virtual_machine and self.server_id:
            try:
                vm = VirtualMachine.objects.get(name=self.server_id)
                self.virtual_machine = vm
            except VirtualMachine.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.src_ip}:{self.src_port} -> {self.dst_ip}:{self.dst_port} ({self.protocol})"