{% raw -%}
# -*- coding: utf-8 -*-
"""
Suministra el estado inicial de un servidor.

- Crear el grupo que realizará el deploy.
- Crear el usuario que realizará el deploy.
- Añadir el grupo a sudoers.
- Crear la clave pública y privada ssh.
- Agregar la public key en el servidor remoto.
- Desactivar el acceso por SSH Password.

"""
import os

from fabric.api import env
from fabric.api import local
from fabric.api import sudo
from fabric.contrib.files import sed


# variables para la creación de clave pública y privada del ssh
abs_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env.ssh_keys_dir = os.path.join(abs_dir_path, 'ssh-keys')

# ssh
env.user = '{{ cookiecutter.provider_user }}'
env.password = '{{ cookiecutter.provider_password }}'
env.hosts = ['{{ cookiecutter.ip_server }}']

# usuario deploy
env.deploy_user = '{{ cookiecutter.deploy_user }}'
env.deploy_group = env.deploy_user


def start():
    """
    Configuración inicial del servidor.
    """
    create_deploy_group()
    create_deploy_user()
    add_group_in_sudoers()
    make_ssh_key()
    upload_key()
    deactivate_ssh_password()


def create_deploy_group():
    """
    Crea un grupo.
    """
    sudo('groupadd {remote_group}'.format(remote_group=env.deploy_group))


def create_deploy_user():
    """
    Crea el deploy user.
    """
    sudo('useradd -m -s /bin/bash -g {remote_group} {remote_user}'.format(
        remote_user=env.deploy_user, remote_group=env.deploy_group))

    sudo('passwd {remote_user}'.format(remote_user=env.deploy_user))

    sudo('usermod -a -G {remote_group} {remote_user}'.format(
        remote_group=env.deploy_group,
        remote_user=env.deploy_user))

    sudo('mkdir /home/{}/.ssh'.format(env.deploy_user))

    sudo('chown -R {remote_user} /home/{remote_user}/.ssh'.format(
        remote_user=env.deploy_user))

    sudo('chgrp -R {remote_group} /home/{remote_user}/.ssh'.format(
        remote_group=env.deploy_group,
        remote_user=env.deploy_user))


def add_group_in_sudoers():
    """
    Añade el grupo a sudoers.
    """
    sudo('cp /etc/sudoers /etc/sudoers-backup')

    # http://stackoverflow.com/a/550808/2655199
    sudo('echo "%{remote_group} ALL=(ALL) ALL" | '
         'tee --append /etc/sudoers'.format(remote_group=env.deploy_group))

    sudo('chmod 440 /etc/sudoers')


def make_ssh_key():
    """
    Creación de clave pública y privada del ssh.
    """
    env.ssh_key_name = os.path.join(
        env.ssh_keys_dir,
        env.host_string + '_prod_key'
    )
    local('ssh-keygen -t ed25519 -f {ssh_key_name}'.format(
        ssh_key_name=env.ssh_key_name))

    local('cp {ssh_key_name} {ssh_keys_dir}/authorized_keys'.format(
        ssh_key_name=env.ssh_key_name + '.pub',
        ssh_keys_dir=env.ssh_keys_dir))


def upload_key():
    """
    Sube la clave pública al servidor remoto.
    """
    scp_command = 'scp {ssh_key_name_pub} {ssh_keys_dir}/authorized_keys ' \
        '{remote_user}@{host_string}:~/.ssh'.format(
            ssh_key_name_pub=env.ssh_key_name + '.pub',
            ssh_keys_dir=env.ssh_keys_dir,
            remote_user=env.deploy_user,
            host_string=env.host_string
        )
    local(scp_command)


def deactivate_ssh_password():
    """
    Desactiva la conexión por medio de ssh password.
    """
    sed('/etc/ssh/sshd_config',
        '^UsePAM yes',
        'UsePAM no',
        use_sudo=True)
    sed('/etc/ssh/sshd_config',
        '^PermitRootLogin yes',
        'PermitRootLogin no',
        use_sudo=True)
    sed('/etc/ssh/sshd_config',
        '^#PasswordAuthentication yes',
        'PasswordAuthentication no',
        use_sudo=True)

    sudo('service sshd reload')

{%- endraw %}
