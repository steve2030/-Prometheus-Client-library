import os
import time
import requests
from prometheus_client import start_http_server, Gauge

# Environment variables for RabbitMQ credentials
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "15672")

# Prometheus metrics
METRICS = {
    "messages": Gauge(
        "rabbitmq_individual_queue_messages",
        "Total number of messages in a RabbitMQ queue",
        ["host", "vhost", "name"],
    ),
    "messages_ready": Gauge(
        "rabbitmq_individual_queue_messages_ready",
        "Number of ready messages in a RabbitMQ queue",
        ["host", "vhost", "name"],
    ),
    "messages_unacknowledged": Gauge(
        "rabbitmq_individual_queue_messages_unacknowledged",
        "Number of unacknowledged messages in a RabbitMQ queue",
        ["host", "vhost", "name"],
    ),
}

def fetch_rabbitmq_metrics():
    """
    Fetch metrics from RabbitMQ HTTP API and update Prometheus Gauges.
    """
    api_url = f"http://{RABBITMQ_HOST}:{RABBITMQ_PORT}/api/queues"
    try:
        # Send a GET request to RabbitMQ management API
        response = requests.get(api_url, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD))
        response.raise_for_status()
        queues = response.json()

        for queue in queues:
            host = RABBITMQ_HOST
            vhost = queue.get("vhost", "default")
            name = queue.get("name", "unknown")

            # Update Prometheus Gauges with RabbitMQ metrics
            METRICS["messages"].labels(host, vhost, name).set(queue.get("messages", 0))
            METRICS["messages_ready"].labels(host, vhost, name).set(queue.get("messages_ready", 0))
            METRICS["messages_unacknowledged"].labels(host, vhost, name).set(queue.get("messages_unacknowledged", 0))

    except requests.RequestException as e:
        print(f"Error fetching RabbitMQ metrics: {e}")

def main():
    """
    Main function to start the Prometheus exporter and scrape metrics periodically.
    """
    # Start Prometheus HTTP server on port 9100
    start_http_server(9100)
    print("Prometheus RabbitMQ Exporter started on port 9100")

    # Scrape metrics every 15 seconds
    scrape_interval = 15
    while True:
        fetch_rabbitmq_metrics()
        time.sleep(scrape_interval)

if __name__ == "__main__":
    main()
