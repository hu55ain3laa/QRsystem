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
```

Make sure your editor is using the correct Python virtual environment, with the interpreter at `backend/.venv/bin/python`.


## To run

use `fastapi run --reload`