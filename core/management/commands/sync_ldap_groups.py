from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django_auth_ldap.backend import LDAPBackend

class Command(BaseCommand):
    help = "Sync LDAP groups to Django groups automatically"

    def handle(self, *args, **kwargs):
        ldap_backend = LDAPBackend()
        connection = ldap_backend.ldap_initialize()

        ldap_backend.ldap_bind(connection)

        self.stdout.write(self.style.SUCCESS("Fetching LDAP groups..."))

        result = connection.search_s(
            "CN=Users,DC=marketplace,DC=local",
            ldap_backend.ldap.SCOPE_SUBTREE,
            "(objectClass=group)",
            ["cn"]
        )

        for dn, entry in result:
            group_name = entry['cn'][0].decode('utf-8')
            Group.objects.get_or_create(name=group_name)
            self.stdout.write(self.style.SUCCESS(f"Synced group: {group_name}"))

        connection.unbind_s()

        self.stdout.write(self.style.SUCCESS("LDAP Groups Synced Successfully!"))
