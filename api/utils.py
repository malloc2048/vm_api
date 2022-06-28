import libvirt
from functools import wraps
from flask import request, abort


def token_required(f):
    """ decorator function to check tokens in header """
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'x-auth' not in request.headers:
            abort(400, 'Token is missing !')
        elif request.headers.get('x-auth') != "s3cret":
            abort(401, 'Invalid token, an unauthorized access to the requested resources.')
        return f(*args, **kwargs)
    return wrapped


def get_vm_info_by_name(vm_name: str):
    conn = None
    domain = None
    try:
        conn = libvirt.open('qemu:///system')
        domain = conn.lookupByName(vm_name)
    except libvirt.libvirtError:
        pass
    finally:
        if conn:
            conn.close()
    return domain


def get_all_vm_details():
    conn = None
    details = None
    try:
        conn = libvirt.open('qemu:///system')
        details = conn.getAllDomainStats()

    except libvirt.libvirtError:
        pass

    finally:
        if conn:
            conn.close()
    return details
