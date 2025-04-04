# FastAPI Project - Backend

## Requirements

* [uv](https://docs.astral.sh/uv/) for Python package and environment management.

## General Workflow

From `./backend/` you can install all the dependencies with:

```console
$ uv sync
```

Then you can activate the virtual environment with:

```console
$ source .venv/bin/activate
on windows
$ .venv\scripts\activate
```

Make sure your editor is using the correct Python virtual environment, with the interpreter at `backend/.venv/bin/python`.


## To run
use `fastapi run --reload`

The admin User

admin@admin.com
admin123

## Docker Setup

This project includes Docker configuration for easy setup and deployment.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running with Docker

1. Build and start the container:

```bash
docker-compose up -d
```

2. Connect to the running container:

```bash
docker-compose exec backend bash
```

3. Once inside the container, set up the environment and run the application:

```bash
# Install dependencies and create virtual environment with uv
uv sync

# Run venv
source .venv/bin/activate

# Run the application
fastapi run --reload
```

### Stopping the Container

```bash
docker-compose down
```

### Development Workflow with Docker

When developing, you can:

1. Edit files on your host machine
2. The changes will be reflected immediately in the container
3. If you add new dependencies to pyproject.toml, run `uv sync` again in the container

This setup keeps your development environment isolated and consistent across different machines.