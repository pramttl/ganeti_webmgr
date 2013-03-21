# Copyright (C) 2012 Oregon State University et al.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

from django.db.models import Q

from object_permissions import get_users_any

from ganeti_web.models import Cluster, ClusterUser, VirtualMachine


def cluster_qs_for_user(user, **kwargs):
    if user.is_superuser:
        qs = Cluster.objects.all()
    elif user.is_anonymous():
        qs = Cluster.objects.none()
    else:
        groups = kwargs.get('groups', True)
        qs = user.get_objects_any_perms(Cluster, ['admin', 'create_vm'],
                                        groups=groups, **kwargs)

    # Exclude all read-only clusters.
    qs = qs.exclude(Q(username='') | Q(mtime__isnull=True))

    return qs


def owner_qs_for_cluster(cluster):
    """
    Get all owners for a cluster.
    """

    # get_users_any() can't deal with None, and at any rate, nobody can
    # possibly own a null cluster.
    if not cluster:
        return ClusterUser.objects.none()

    # Get all superusers.
    qs = ClusterUser.objects.filter(profile__user__is_superuser=True)

    # Get all users who have the given permissions on the given cluster.
    users = get_users_any(cluster, ["admin"], True)
    qs |= ClusterUser.objects.filter(profile__user__in=users)

    return qs


def vm_qs_for_admins(user):
    """
    Retrieve a queryset of all of the virtual machines for which this user is
    an administrator.
    """

    if user.is_superuser:
        qs = VirtualMachine.objects.all()
    elif user.is_anonymous():
        qs = VirtualMachine.objects.none()
    else:
        qs = user.get_objects_any_perms(VirtualMachine, groups=True,
                                        perms=["admin"])

    return qs

def vm_qs_for_users(user):
    """
    Retrieves a queryset of all the virtual machines for which the user has
    any permission.
    """

    if user.is_superuser:
        qs = VirtualMachine.objects.all()
    elif user.is_anonymous():
        qs = VirtualMachine.objects.none()
    else:
        # If no permissions are listed, then *any* permission will cause a VM
        # to be added to the query.
        qs = user.get_objects_any_perms(VirtualMachine, groups=True)

    return qs
