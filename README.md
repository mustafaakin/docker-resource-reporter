docker-resource-reporter
========================

Reports the resource usage of Docker containers to InfluxDB

## Installation

```sh

pip install pyyaml influxdb

```

Also you need to have created a InfluxDB already, this code does not create the database for you.

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


## Sample Queries


### The memory usage of containers over time

```sql
SELECT rss FROM /.*memory/ GROUP BY time(15s)
```

![memory](https://raw.githubusercontent.com/mustafaakin/docker-resource-reporter/master/examples/memory.png)

### CPU utilization, time spent in all CPUs (time in nanoseconds)

```sql
SELECT derivative(Total) FROM /.*cpu/ GROUP BY time(5s) 
```
![cpu](https://raw.githubusercontent.com/mustafaakin/docker-resource-reporter/master/examples/cpu.png)

Note: I had a 8 core machine, so 8M means it spent 8million nanoseconds = 8 seconds, meaning it was full utilization

### Bytes read/write speed from/to Disk 

```sql
SELECT Derivative(Total) FROM /.*disk.bytes/ GROUP BY time(5s)
```

![memory](https://raw.githubusercontent.com/mustafaakin/docker-resource-reporter/master/examples/bytes.png)

### Number of Asynchronous IO Requests

```sql
SELECT Async FROM /.*disk.count/
```

![memory](https://raw.githubusercontent.com/mustafaakin/docker-resource-reporter/master/examples/async.png)

Note: It is the sum of values, not the speed. If you want speed, you have to take the derivative of the values by derivative() operator.