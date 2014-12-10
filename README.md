docker-resource-reporter
========================

Reports the resource usage of Docker containers to InfluxDB

## Installation

```sh
pip install pyyaml influxdb
```

Also you need to have created a InfluxDB database already, this code does not create the database for you.

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

The metrics are stored in the given database as: HOST.CONTAINERID.cpu, HOST.CONTAINERID.memory,  HOST.CONTAINERID.disk.bytes, HOST.CONTAINERID.disk.counts . This is the recommended way in the InfluxDB documentation, storing the host & containerid as a row is also possible but seems to be slow. Although, you are free to modify the code to suit your needs.

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

Note: I run a 4 core VM under VirtualBox, 1G means = 1 second, I run `sysbench --test=cpu --cpu-max-prime=50000 --num-threads=1` then canceled it and run it with 2, 4 and 32 threads to show that 2G means 2 second consumed in total, and 4G means 4 second consumed, and if we have more threads the performance drops a little because of switching cost, it is not full 4G. Anyways, it should indicate

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

## TODO

- A nice UI that repeats the queries over time and plots them in a nicer way.