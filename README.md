# Template Cookiecutter para Suministro de Proyecto Base

## Intro

Este template de [Cookiecutter](https://github.com/audreyr/cookiecutter) tiene por objetivo crear un proyecto base para montar aplicaciones en [Django](https://github.com/django/django) en un VPS.

## Caracteristicas
- Docker
- Nginx
- Postgres
- Certbot

## Init
Instalar [Cookiecutter](https://github.com/audreyr/cookiecutter):

```
$ pip install "cookiecutter>=1.4.0"
```

Luego, aplicar:

```
$ cookiecutter https://github.com/NekoTashi/template-suministro-proyecto-base.git
```


### Variables Cookiecutter Template

Variable | Descripción
--- | ---
`project_name` | Nombre del proyecto.
`repo_name` | Nombre del proyecto generado a partir de `project_name`.
`provider_user` | Usuario SSH que se crea por defecto al momento de montar un servidor.
`provider_password` | Password SSH que se crea por defecto al momento de montar un servidor.
`ip_server` | IP del Servidor a suministrar.
`deploy_user` | Usuario que hará el diploy de la aplicación en el servidor.
`db_password` | Password de la base de datos.
`postgres_version` | Versión de PostgreSQL.
