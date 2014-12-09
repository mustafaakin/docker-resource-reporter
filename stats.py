from Docker import *
from InfluxDBReporter import *

docker = Docker("http://localhost:4500")
containers = docker.getContainers()

influx = InfluxDBReporter("localhost", "root", "root", 8086, "docker")

for container in containers:	
	id = container["Id"];
	name = container["Names"][0]
	print id, name

	io = docker.ioStats(id)
	cpu = docker.cpuStats(id);
	memory = docker.memoryStats(id);

	influx.reportMemory(id, memory)
	influx.reportCpu(id, cpu)
	influx.reportIO(id,io)