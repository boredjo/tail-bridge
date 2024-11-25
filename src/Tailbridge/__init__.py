import docker
import subprocess
import time

from . import tailscale

# Connect to the Docker daemon
client = docker.from_env()
        
def handle_container_event(event):
    """Handle the start event for a container."""
    try:
        container_id = event['id']
        container = client.containers.get(container_id)
        labels = container.labels

        # Check if the container has the Tailscale label
        if labels.get("tailbridge.enable") == "true":
            print(f"Configuring Tailscale for container {container.name}")

            tailscale.install(container)
                
            # service_name = labels.get("tailbridge.traefik.service")
                
            # if service_name is not None:
            #     time.sleep(2)
            #     result = container.exec_run("sh -c 'tailscale ip -4'")
            #     tailscale_ip = result.output.decode("utf-8").strip()
            #     print(f"Tailscale IP of {container.name} is {tailscale_ip}")
            #     port = labels.get(f"traefik.http.services.{service_name}.loadbalancer.server.port")
            #     labels = container.labels.copy()
            #     labels[f"traefik.http.service.{service_name}.loadbalancer.server.url"] = f"http://{tailscale_ip}:{port}"
            #     container.update(labels=labels)
        
            print(f"Tailscale configured for container {container.name}")
            print(f"Tailscale Ip is {tailscale.get_ip(container)}")

    except Exception as e:
        print(f"Error handling container {event['id']}: {e}")
    

def run_tailbridge():
    # Listen to Docker events
    print("Listening for Docker events...")
    for event in client.events(decode=True):
        if event.get("Type") == "container" and event.get("Action") == "start":
            handle_container_event(event)
