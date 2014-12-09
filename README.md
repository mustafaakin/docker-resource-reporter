docker-resource-reporter
========================

Reports the resource usage of Docker containers to InfluxDB

## Usage

```sh

python report.py 

```

For continous reporting with 5 seconds interval:

```sh

watch python report.py

```

## Config

Edit the `config.yaml` file to config your InfluxDB parameters and Docker Remote API endpoint. Currently, Unix socket binded Docker remote API is not tried.

```yaml

docker:
    api: "http://localhost:4500"
influxdb:
    host: localhost
    user: root
    password: root
    port: 8086
    database: docker

```
