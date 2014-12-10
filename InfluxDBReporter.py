from influxdb import InfluxDBClient
import socket

class InfluxDBReporter:
	"""Simple class to report the metrics to InfluxDB"""

	def __init__(self, host, username, password, port, database):
		# Construct a InfluxDB client and our localhost name to report to the server
		self.client = InfluxDBClient(host, port, username, password, database)
		self.hostname = socket.gethostname()

	def reportIO(self, id, metrics):
		# First for bytes
		b = metrics["bytes"]
		json_body = [{
		    "points": [
		       [b["Read"], b["Write"], b["Total"], b["Sync"], b["Async"]]
		    ],
		    "name": self.hostname + "."  + id + ".disk.bytes",
		    "columns": ["Read", "Write", "Total", "Sync", "Async"]
		}]
		self.client.write_points(json_body)

		# Then for IO request counts
		c = metrics["count"]
		json_body = [{
		    "points": [
		       [c["Read"], c["Write"], c["Total"], c["Sync"], c["Async"]]
		    ],
		    "name": self.hostname + "."  + id + ".disk.count",
		    "columns": ["Read", "Write", "Total", "Sync", "Async"]
		}]
		self.client.write_points(json_body)


	def reportCpu(self, id, metrics):
		points = [metrics["total"]]
		columns = ["Total"]
		
		# There might be many cpus, store values as CPU0-value, CPU1-value..
		for idx, cpu in enumerate(metrics["cpus"]):
			points.append(cpu)
			columns.append("CPU" + str(idx))

		json_body = [{
		    "points": [points],
		    "name": self.hostname + "."  + id + ".cpu",
		    "columns": columns
		}]

		self.client.write_points(json_body)

	def reportMemory(self, id, metrics):		
		points = []
		columns = []

		# Iterates over all memory metrics, can be altered to report only specific fields such as rss
		for key, value in metrics.iteritems():
			points.append(value)
			columns.append(key)

		json_body = [{
		    "points": [points],
		    "name": self.hostname + "."  + id + ".memory",
		    "columns": columns
		}]


		self.client.write_points(json_body)		