
import docker
import os

def install(container, verbose=True):
    try:
        _install_curl(container, verbose)
        _install_with_script(container, verbose)
    except docker.errors.NotFound:
        print("Container not found.")
    except docker.errors.APIError as e:
        print(f"Error communicating with the Docker API: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def _install_curl(container, verbose=True)
    if container.exec_run("sh -c 'apt update'", stdout=True, stderr=True).exit_code == 0:
        # apt is installed
        if verbose: print("Installing curl with apt")
        result = container.exec_run("sh -c 'apt install curl -y'",  stdout=True, stderr=True)
    elif container.exec_run("sh -c 'apk update'", stdout=True, stderr=True).exit_code == 0:
        # apk is installed
        if verbose: print("Installing curl with apk")
        result = container.exec_run("sh -c 'apk install curl -y'",  stdout=True, stderr=True)
    else:
        print("This Container is not supported at the moment")


def _install_with_script(container, verbose=True):
    container.exec_run(
        "sh -c '"
        "curl -fsSL https://tailscale.com/install.sh | sh && "
        "tailscaled --state=/var/lib/tailscale/tailscaled.state"
        "'"
    )
    if verbose: print("Tailscale is installed")


def login(container, verbose=True):
    container.exec_run(
        "sh -c '"
        "tailscale up "
        f"--authkey={os.environ['TS_AUTHKEY']} "
        f"--hostname={container.name} "
        f"--accept-dns={os.environ['TS_ACCEPT_DNS']}"
        os.environ['TS_EXTRA_ARGS']
        detach=True
    )



def get_ip(container):
    try:
        result = container.exec_run("sh -c 'tailscale ip -4'")
        return result.output.decode("utf-8").strip()
    except docker.errors.NotFound:
        print("Container not found.")
    except docker.errors.APIError as e:
        print(f"Error communicating with the Docker API: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
