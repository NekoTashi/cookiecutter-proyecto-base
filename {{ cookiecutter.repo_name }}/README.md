# Proyecto Base

## Init

Antes de realizar el suministro con [Ansible](https://github.com/ansible/ansible) al servidor, se deberá aplicar [Fabric](https://github.com/fabric/fabric) para:

- Crear el grupo que realizará el deploy.
- Crear el usuario que realizará el deploy.
- Añadir el grupo a sudoers.
- Crear la clave pública y privada ssh.
- Agregar la public key en el servidor remoto.
- Desactivar el acceso por SSH Password.

## Fabric

Dentro de la carpeta `fabric/`, aplicar:
```
fab start
```

Nota: Pedirá que se proporcione la password del `deploy_user`.

## Ansible

Luego de aplicado [Fabric](https://github.com/fabric/fabric), se debe ejecutar el siguiente comando dentro de la carpeta `ansible/`:

- `ansible-playbook -i development site.yml --ask-become-pass`.
- `--ask-become-pass` pedirá la password del `deploy_user`.
