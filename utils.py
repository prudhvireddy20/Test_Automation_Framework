import logging
import sys


def setup_logging(level_str: str = "INFO") -> None:

    level = getattr(logging, level_str.upper(), logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.getLogger().info("Logging initialized at %s level", level_str.upper())



def mock_ssh(host: str) -> bool:

    logging.getLogger("mock_ssh").debug("Connecting via SSH to %s", host)
    print(f"[MOCK] SSH connection established to {host}")
    return True


def mock_rdp(host: str) -> bool:

    logging.getLogger("mock_rdp").debug("Connecting via RDP to %s", host)
    print(f"[MOCK] RDP session validated for {host}")
    return True
