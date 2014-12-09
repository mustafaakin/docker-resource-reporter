import urllib2
import json
from influxdb import InfluxDBClient

api = 'http://localhost:4500/';

def getLines(filename):
	f = open(filename)
	lines = [line.rstrip('\n') for line in open(filename)]
	f.close()
	return lines

def ioStats(id):
	metrics = []
	metrics.append({'filename':"blkio.throttle.io_service_bytes", 'name':"bytes"}) 
	metrics.append({'filename':"blkio.throttle.io_serviced", 'name':"count"}) 

	results = {}
	for metric in metrics:
		lines = getLines("/sys/fs/cgroup/blkio/docker/" + id + "/" + metric["filename"])
		reqs = {};
		for line in lines:
			line = line.split()
			if (len(line) == 3):
				reqs[line[1]] = int(line[2])
			elif (len(line) == 2):
				reqs[line[0]] = int(line[1])
		results[metric["name"]] = reqs
	return results

def cpuStats(id):
	values = [int(value) for value in getLines("/sys/fs/cgroup/cpuacct/docker/" + id + "/cpuacct.usage_percpu")[0].split()]
	total = 0
	for value in values:
		total = total + value
	resp = {'total': total, 'cpus': values} 
	return resp

def memoryStats(id):
	lines = getLines("/sys/fs/cgroup/memory/docker/" + id + "/memory.stat")
	resp = {}
	for line in lines:
		line = line.split()
		resp[line[0]] = int(line[1])

	return resp

# InfluxDB init
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'docker')
# Parse all the things
response = urllib2.urlopen(api + "/containers/json");
data = json.load(response) 
for container in data:
	id = container["Id"]
	name = container["Names"][0]
	print "Container", id, "name", name
	# print(ioStats(id))
	# print(cpuStats(id))
	# print(memoryStats(id))
	# q = cpuStats(id)
	q = ioStats(id)["bytes"]
	print(q)
	json_body = [{
	    "points": [
	       [id, q["Read"], q["Write"], q["Total"], q["Sync"], q["Async"]]
	    ],
	    "name": "disk",
	    "columns": [id, "Read", "Write", "Total", "Sync", "Async"]
	}]
	print(json_body)
	client.write_points(json_body)