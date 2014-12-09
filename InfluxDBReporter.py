from influxdb import InfluxDBClient
import socket

class InfluxDBReporter:
	"""Simple class to report the metrics to InfluxDB"""

	def __init__(self, host, username, password, port, database):
		self.client = InfluxDBClient(host, port, username, password, database)
		self.hostname = socket.gethostname()

	def reportIO(self, id, metrics):
		b = metrics["bytes"]
		c = metrics["count"]

		json_body = [{
		    "points": [
		       [self.hostname, id, b["Read"], b["Write"], b["Total"], b["Sync"], b["Async"]]
		    ],
		    "name": "disk.bytes",
		    "columns": ["hostname", "ID", "Read", "Write", "Total", "Sync", "Async"]
		}]
		self.client.write_points(json_body)


		json_body = [{
		    "points": [
		       [self.hostname, id, c["Read"], c["Write"], c["Total"], c["Sync"], c["Async"]]
		    ],
		    "name": "disk.count",
		    "columns": ["hostname", "ID", "Read", "Write", "Total", "Sync", "Async"]
		}]
		self.client.write_points(json_body)


	def reportCpu(self, id, metrics):
		points = [id, self.hostname, metrics["total"]]
		columns = ["ID", "hostname", "Total"]
		for idx, cpu in enumerate(metrics["cpus"]):
			points.append(cpu)
			columns.append("CPU" + str(idx))

		json_body = [{
		    "points": [points],
		    "name": "cpu",
		    "columns": columns
		}]

		self.client.write_points(json_body)

	def reportMemory(self, id, metrics):
		points = [id, self.hostname]
		columns = ["ID", "hostname"]
		for key, value in metrics.iteritems():
			points.append(value)
			columns.append(key)

		json_body = [{
		    "points": [points],
		    "name": "memory",
		    "columns": columns
		}]


		self.client.write_points(json_body)		