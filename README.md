# Prometheus Target Exporter

Exporting metrics about prometheus targets (for now only down target count)

## Using Docker

You can deploy this exporter using the [ekesken/prom-target-exporter](https://registry.hub.docker.com/u/ekesken/prom-target-exporter/) Docker image.

For example:

```bash
docker run -d -e PROM_TARGET_ENDPOINT=http://server-prom.marathon.mesos:9090/targets -p 9099:9099 ekesken/prom-target-exporter
# try it
# curl http://localhost:9099/metrics
```

## Deploy on Marathon

You can deploy this exporter on marathon via following curl command:

```bash
curl -XPOST -H 'Content-Type: application/json;' marathon.mesos:8080/v2/apps -d '{
  "cpus": 0.01,
  "mem": 100,
  "id": "/prom/target-exporter",
  "instances": 1,
  "env": {
    "PROM_TARGET_ENDPOINT": "http://server-prom.marathon.mesos:9090/targets"
  },
  "container": {
    "type": "DOCKER",
    "docker": {
      "image": "ekesken/prom-target-exporter",
      "network": "BRIDGE",
      "privileged": true,
      "portMappings": [{"containerPort": 9099}]
    }
  },
  "healthChecks": [{"protocol": "HTTP", "path": "/metrics"}]
}'
```

## Scrape config on prometheus

A sample prometheus target yaml example if you already have have mesos-dns:

```
  - job_name: 'target'
    dns_sd_configs:
      - names: ['_target-exporter-prom._tcp.marathon.mesos']
```
