#!/usr/bin/env python3
import binascii
import yaml
import os
import sys
import base64

print('Loading database')
pkg_db_file = open('sample.yml', 'r')
pkg_db = yaml.safe_load(pkg_db_file)
RUNDIR = os.path.dirname(__file__)
packages_path = os.path.join(RUNDIR, 'packages')
if not os.path.isdir(packages_path):
    os.makedirs(packages_path, exist_ok=False)
pid = sys.argv[1]


def acquiring_mkdir(pid: str, pkg_def):
    global packages_path
    if pkg_def['type'] == 'DIRECTORY':
        dirpath = os.path.join(packages_path, pkg_def['name'])
        print('Creating {}'.format(str(dirpath)))
        os.makedirs(dirpath, exist_ok=True)


def acquiring_ipfs_file(pid: str, pkg_def):
    import urllib.parse
    base_url = 'https://ipfs.robotics.bmstu.ru/ipfs/' + pid + '?filename=' + urllib.parse.quote_plus(pkg_def['name'])
    print('Acquiring GET on base URL {}'.format(base_url))
    os.system('curl --output \'{}\' {}'.format(os.path.join(packages_path, pkg_def['name']), base_url))


def control_base64name(pid: str, pkg_def):
    hash = pid.encode('iso-8859-1')
    try:
        if base64.b64decode(hash).decode('iso-8859-1') == pkg_def['name']:
            print('PID \'{}\' reproduced with custom Base64 integrity control subroutine'.format(hash.decode(
                'iso-8859-1')))
            return True
        else:
            return False
    except binascii.Error:
        return False


def control_ipfs(pid, pkg_def):
    return True    # Just the stub to not implement the node on the client side


acquiring_subroutines_avail = {"DIRECTORY": acquiring_mkdir,
                               "IPFS FILE": acquiring_ipfs_file}
control_subroutines_avail = {'base64_name': control_base64name,
                             'IPFS FILE': control_ipfs}


def resolve_local(pid):
    global pkg_db, \
        acquiring_subroutines_avail, \
        control_subroutines_avail
    resolved = False
    if pid in pkg_db:
        print('Resolved as local entry')
        resolved = True
        acquiring_subroutine = None
        control_subroutine = None
        if pkg_db[pid]['acquiring_subroutine_override'] is not None:
            acquiring_subroutine = acquiring_subroutines_avail[pkg_db[pid]['acquiring_subroutine_override']]
        else:
            if pkg_db[pid]['type'] in acquiring_subroutines_avail.keys():
                acquiring_subroutine = acquiring_subroutines_avail[pkg_db[pid]['type']]
        if pkg_db[pid]['integrity_control_subroutine_override'] is not None:
            control_subroutine = control_subroutines_avail[pkg_db[pid]['integrity_control_subroutine_override']]
        else:
            if pkg_db[pid]['type'] in control_subroutines_avail.keys():
                control_subroutine = control_subroutines_avail[pkg_db[pid]['type']]
        return resolved, pkg_db[pid], acquiring_subroutine, control_subroutine
    else:
        print('PID {} not resolved as local entry'.format(pid))
        return tuple([resolved])


def resolve_false(pid):
    # Demo stub to demonstrate resolving sequence
    return tuple([False])


resolvers_avail = [resolve_false,
                   resolve_local]


def deploy_package(pid):
    print('===\nPID to resolve: {}'.format(pid))
    print('Entering RESOLVING stage')
    for resolver in resolvers_avail:
        resolved = resolver(pid)
        if resolved[0]:
            pkg_def = resolved[1]
            if resolved[2] is None or resolved[3] is None:
                raise OSError('Persistent ID cannot be resolved, please check the database')
            print('NOTE: customized PREDEPLOYMENT and POSTDEPLOYMENT stages are not implemented in this demo')
            print('Entering PREDEPLOYMENT stage')
            if pkg_def['dependencies'] is not None and len(pkg_def['dependencies']) > 0:
                print('Dependencies detected, turning on recursion')
                for i in pkg_def['dependencies']:
                    deploy_package(i)
            print('Dependencies deployed, entering ACQUIRING stage with subroutine {}'.format(resolved[2].__name__))
            acquiring_subroutine = resolved[2]
            acquiring_subroutine(pid, pkg_def)
            print('Entering INTEGRITY CONTROL stage')
            control_subroutine = resolved[3]
            if control_subroutine(pid, pkg_def):
                print('Package {} data considered deployed'.format(pkg_def['name']))
            else:
                print('Error occurred deploying package {}!'.format(pkg_def['name']))
            break
        else:
            print('Resolver \'{}\' cannot resolve the PID, passing to the next available resolver'.format(
                resolver.__name__))


deploy_package(pid)
print('DEMO: fake POSTDEPLOYMENT stage')
os.rename(os.path.join(packages_path, 'Knowledge Packages [2021-04-15].mp4'),
          os.path.join(os.path.join(packages_path, 'Knowledge Packages - Presentation Video'),
                       'Knowledge Packages [2021-04-15].mp4'))
pkg_db_file.close()

