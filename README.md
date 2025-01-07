# Prometheus RabbitMQ Exporter

This project provides a Prometheus exporter written in Python that connects to a RabbitMQ HTTP API (Management Plugin) and periodically collects metrics about all queues in all vhosts. The exporter then exposes these metrics in a Prometheus-compatible format.

The exporter collects and exposes the following RabbitMQ metrics:
- **Total number of messages**: `rabbitmq_individual_queue_messages{host,vhost,name}`
- **Number of ready messages**: `rabbitmq_individual_queue_messages_ready{host,vhost,name}`
- **Number of unacknowledged messages**: `rabbitmq_individual_queue_messages_unacknowledged{host,vhost,name}`

Each metric is labeled with:
- `host`: RabbitMQ hostname
- `vhost`: RabbitMQ virtual host
- `name`: Queue name

Ensure the RabbitMQ Management Plugin is enabled. Run:
```bash
rabbitmq-plugins enable rabbitmq_management
