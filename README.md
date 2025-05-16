<div align="center">

# Heartmeter
## Blood pressure diary

[![python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![UV](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

</div>

### Services
- **Diary**
- **Reporter**
- **Weather**

### Run

```shell
docker compose --profile heartmeter up --build -d
```

#### `Swagger:` http://127.0.0.1:8080/docs/

### Stop
```shell
docker compose --profile heartmeter down
```

### Start the load
Install Grafana [k6](https://grafana.com/docs/k6/latest/set-up/install-k6/)

```shell
k6 run k6/load.js
```
