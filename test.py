import yaml
f = open('config.yaml')
# use safe_load instead load
dataMap = yaml.safe_load(f)
f.close()
print dataMap