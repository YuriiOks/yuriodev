import docker
import time
import logging
import io

logger = logging.getLogger(__name__)

# Configuration for the sandbox
PYTHON_IMAGE = "python:3.10-slim" # Use a specific, minimal image
DEFAULT_TIMEOUT_SECONDS = 5 # Max execution time
MAX_OUTPUT_SIZE = 1024 * 5 # Max output size in bytes (5KB) to prevent abuse

# It's good practice to initialize the Docker client once
try:
    docker_client = docker.from_env()
except docker.errors.DockerException:
    logger.error("Could not connect to Docker daemon. Is Docker running and accessible?")
    docker_client = None # Handle this gracefully in run_python_code


def run_python_code(code: str) -> dict:
    if not docker_client:
        return {
            "output": "",
            "error": "Code execution service is not available (Docker connection failed).",
            "execution_time": 0,
            "success": False,
        }

    # Prepare the command to execute the Python code
    # Using python -c "code" is simple but can have issues with complex quotes or multiline.
    # A more robust way is to write code to a temp file and execute it, but that requires volume mounts.
    # For this MVP, python -c should suffice for simple snippets.
    # Ensure code is properly escaped if directly embedded, though SDK handles this.
    command = ["python", "-c", code]

    # Non-root user, e.g., 'nobody' (UID 65534) or a specific user in the image
    # Python slim images run as root by default. For better security, a custom image
    # with a non-root user or using `user` param with existing UID is needed.
    # For 'python:3.10-slim', 'nobody' might not exist or have write perms for /tmp if needed.
    # Let's assume for MVP we run as default user in container, but note this for hardening.
    # user_to_run_as = "nobody"
    user_to_run_as = None # Default (root in python:slim) for now. Add custom image later.


    container = None
    start_time = time.time()
    try:
        container = docker_client.containers.run(
            image=PYTHON_IMAGE,
            command=command,
            detach=True, # Run in background
            # Security settings:
            network_disabled=True, # No network access
            # network_mode='none', # Alternative for disabling network
            mem_limit="64m", # Memory limit (e.g., 64MB)
            # cpu_shares=512, # Relative CPU weight (optional, default 1024)
            # cpuset_cpus="0", # Pin to specific CPU core(s) (optional)
            # Security options for more hardening (might require specific Docker setup)
            # security_opt=["no-new-privileges"],
            # cap_drop=["ALL"], # Drop all capabilities
            # Read-only root filesystem (if code doesn't need to write)
            # read_only=True,
            # tmpfs={"/tmp": "size=1M,mode=1777,noexec,nosuid"}, # Small, non-executable tmpfs
            user=user_to_run_as,
            # For removing container after it exits
            auto_remove=False, # Set to False to inspect logs/errors, then remove manually
            # stdout=True, stderr=True # Already default
        )

        # Wait for container to finish, with timeout
        try:
            result = container.wait(timeout=DEFAULT_TIMEOUT_SECONDS)
            exit_code = result.get("StatusCode", -1)
        except Exception as e: # Catches requests.exceptions.ReadTimeout or ConnectionError
            # Container timed out or connection issue
            container.kill() # Ensure container is stopped if it timed out
            execution_time = time.time() - start_time
            return {
                "output": "",
                "error": f"Execution timed out after {DEFAULT_TIMEOUT_SECONDS} seconds.",
                "execution_time": round(execution_time, 3),
                "success": False,
            }

        execution_time = time.time() - start_time

        # Fetch logs, limiting output size
        stdout_stream = container.logs(stdout=True, stderr=False, stream=False) # Get as bytes
        stderr_stream = container.logs(stdout=False, stderr=True, stream=False) # Get as bytes

        # Decode and truncate
        stdout = stdout_stream.decode('utf-8', errors='replace')[:MAX_OUTPUT_SIZE]
        stderr = stderr_stream.decode('utf-8', errors='replace')[:MAX_OUTPUT_SIZE]

        if len(stdout_stream) > MAX_OUTPUT_SIZE:
            stdout += "\n[Output truncated]"
        if len(stderr_stream) > MAX_OUTPUT_SIZE:
            stderr += "\n[Error output truncated]"


        success = exit_code == 0 and not stderr # Consider successful if exit code is 0 and no stderr

        return {
            "output": stdout,
            "error": stderr,
            "execution_time": round(execution_time, 3),
            "success": success,
            "exit_code": exit_code
        }

    except docker.errors.ImageNotFound:
        logger.error(f"Docker image {PYTHON_IMAGE} not found.")
        return {"output": "", "error": "Code execution environment error (image not found).", "execution_time": 0, "success": False}
    except docker.errors.APIError as e:
        logger.error(f"Docker API error: {e}")
        return {"output": "", "error": f"Code execution service error (Docker API: {e}).", "execution_time": 0, "success": False}
    except Exception as e:
        logger.error(f"An unexpected error occurred in run_python_code: {e}")
        return {"output": "", "error": "An unexpected server error occurred during code execution.", "execution_time": 0, "success": False}
    finally:
        if container:
            try:
                container.remove(force=True) # Ensure container is removed
            except docker.errors.NotFound:
                pass # Container already removed or failed to create
            except Exception as e:
                logger.error(f"Error removing container {container.id if hasattr(container, 'id') else 'unknown'}: {e}")
