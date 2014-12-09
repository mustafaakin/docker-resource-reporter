from Docker import *
from InfluxDBReporter import *
import yaml

# Open the config to figure out the connection details
f = open('config.yaml')
config = yaml.safe_load(f)
f.close()

# Connect to Docker Remote API to query the containers
docker = Docker( config["docker"]["api"])
containers = docker.getContainers()

# Create InfluxDBReporter
influx = InfluxDBReporter(config["influxdb"]["host"], config["influxdb"]["user"], config["influxdb"]["password"], config["influxdb"]["port"], config["influxdb"]["database"])

for container in containers:	
	id = container["Id"];
	name = container["Names"][0]
	print id, name

	# Get stats from Cgroups files in /sys/fs/cgroup/.. 
	# Paths are different in CoreOS and Ubuntu, do not know really why 
	io = docker.ioStats(id)
	cpu = docker.cpuStats(id);
	memory = docker.memoryStats(id);

	# Report the metrics to database
	influx.reportMemory(id, memory)
	influx.reportCpu(id, cpu)
	influx.reportIO(id,io)