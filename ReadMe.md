## Basic structure for using fastapi

How to run application
- uvicorn main:app --host 127.0.0.1 --port 8000

Packages and Dependency built-ins (optional: remove unwanted resources)
- FastAPI
- Bootstrap 5
- Font Awesome
- Jinja2
- Docker
- Podman
- Env Files
- Kubernetes
- Aws
- Azure
- Heroku
- Vercel

### Hosted Endpoints
- https://vercel.com/tjaskot/aci-portal
- https://aci-portal-tjaskot.vercel.app/index

### Architecture Digrams

- ![Server Architecture](./resources/images/Server%20Architecture.PNG)
- ![Flask Architecture](./resources/images/flask%20api%20architecture.jpg)
- ![Proxy Config](./resources/images/ProxyConfig.jpg)

### Directory Structure

- **app** - to contain python code and FastAPI framework
- **kustomize** - for kubernetes resources and deployment files
- **resources** - word documents and any references to be used for documentation purposes and user assistance
- **Containerfile** - podman container builds
- **Dockerfile** - container build image file for Docker
- **Pipfile** - python pipenv file for server ecosystem
- **Pipfile.lock** - python pipenv lock file for packages, dependencies, and versions
- **Procfile** - open source cloud foundry deployments on Heroku
- **requirements.txt** - if Pipenv is not supported on local machine, 
use "pipenv freeze > requirments.txt" and leverage accordingly
- **vercel.json** - python deployment file for vercel cloud applications