import argparse
import logging
import signal
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Optional

import yaml

from api_client import APIClient
from runner import TestRunner
from utils import setup_logging


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    return cfg


def retry(func, max_attempts: int = 3, backoff: float = 0.5):
    def wrapper(*args, **kwargs):
        attempt = 0
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                attempt += 1
                if attempt >= max_attempts:
                    raise
                wait = backoff * (2 ** (attempt - 1))
                logging.debug("Retrying %s after error: %s (attempt %d), sleeping %.2fs", func.__name__, exc, attempt, wait)
                time.sleep(wait)

    return wrapper


@retry
def ensure_auth(client: APIClient, cfg: Dict[str, Any]) -> str:
    creds = cfg.get("credentials")
    if not creds:
        raise ValueError("No credentials found in config under 'credentials'")

    username = creds.get("username")
    password = creds.get("password")
    if not username or not password:
        raise ValueError("Both 'username' and 'password' must be set in credentials")

    # Register, ignore failure (user may already exist)
    try:
        client.register(username, password)
        logging.info("Registered user %s", username)
    except Exception as e:  # pragma: no cover - preserve behavior
        logging.debug("Register likely already done or failed: %s", e)

    token = client.login(username, password)
    logging.info("Logged in as %s", username)
    return token


def run_parallel(cfg_path: str, workers: Optional[int] = None, dry_run: bool = False) -> Dict[str, Any]:
    cfg = load_config(cfg_path)

    log_level = cfg.get("logging", {}).get("level", "INFO")
    setup_logging(log_level)

    base_url = cfg.get("base_url")
    if not base_url:
        raise ValueError("base_url is required in config.yml")

    client = APIClient(base_url)
    ensure_auth(client, cfg)

    # Prepare test cases
    test_cases = cfg.get("test_cases")
    if not test_cases:
        # default single test using the configured target_vs_name
        test_cases = [{"name": "single", "target_vs_name": cfg.get("target_vs_name")}]

    for i, tc in enumerate(test_cases):
        if not isinstance(tc, dict) or "name" not in tc:
            raise ValueError(f"test_cases[{i}] must be a mapping with at least a 'name' key")

    results: Dict[str, Any] = {}
    runner = TestRunner(client, cfg)

    concurrency = workers or cfg.get("concurrency") or 2
    concurrency = max(1, int(concurrency))

    if dry_run:
        logging.info("Dry-run: would run %d test case(s) with concurrency=%d", len(test_cases), concurrency)
        for tc in test_cases:
            logging.info("Planned test: %s", tc.get("name"))
        return {tc.get("name"): "dry-run" for tc in test_cases}

    stop = False

    def _signal_handler(signum, frame):
        nonlocal stop
        logging.warning("Received signal %s, shutting down executor...", signum)
        stop = True

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    logging.info("Starting %d worker(s)", concurrency)

    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = {ex.submit(runner.run_case, tc): tc for tc in test_cases}

        try:
            for fut in as_completed(futures):
                if stop:
                    logging.warning("Shutdown requested: cancelling remaining futures")
                    break

                tc = futures[fut]
                name = tc.get("name")
                try:
                    res = fut.result()
                    results[name] = res
                    logging.info("Test '%s' finished: %s", name, res)
                except Exception:
                    results[name] = False
                    logging.exception("Test '%s' failed", name)
        finally:
            if stop:
                for f in futures:
                    if not f.done():
                        f.cancel()
                logging.info("Cancelled outstanding tasks")

    return results


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="main.py", description="Parallel test runner for automation-framework")
    p.add_argument("--config", "-c", default="config.yml", help="Path to YAML config")
    p.add_argument("--workers", "-w", type=int, help="Override concurrency/workers (int)")
    p.add_argument("--dry-run", action="store_true", help="Validate config and show planned tests without executing")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    try:
        out = run_parallel(args.config, workers=args.workers, dry_run=args.dry_run)
        print("Results:", out)
    except Exception as exc:  
        logging.exception("Fatal error running tests: %s", exc)
        sys.exit(1)
