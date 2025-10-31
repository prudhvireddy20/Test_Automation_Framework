import logging
import time
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def _retry(fn, attempts: int = 3, backoff: float = 0.5):
    def wrapper(*args, **kwargs):
        last_exc = None
        for attempt in range(1, attempts + 1):
            try:
                return fn(*args, **kwargs)
            except Exception as exc:
                last_exc = exc
                if attempt == attempts:
                    logger.debug("Retry wrapper exhausted for %s", fn.__name__)
                    raise
                wait = backoff * (2 ** (attempt - 1))
                logger.debug("Error in %s: %s (attempt %d/%d) — sleeping %.2fs",
                             fn.__name__, exc, attempt, attempts, wait)
                time.sleep(wait)
        if last_exc:
            raise last_exc
    return wrapper


class TestRunner:

    def __init__(self, client, cfg: Dict[str, Any]):
        self.client = client
        self.cfg = cfg

    @staticmethod
    def _normalize_vs_list(vs_list: Any) -> List[Dict[str, Any]]:
        if isinstance(vs_list, list):
            return vs_list
        if isinstance(vs_list, dict):
            results = vs_list.get("results")
            if isinstance(results, list):
                return results
        
            values = list(vs_list.values())
            if values and isinstance(values[0], dict):
                return [v for v in values if isinstance(v, dict)]
        return []

    def find_vs_by_name(self, vs_list: Any, target_name: str) -> Optional[Dict[str, Any]]:
        items = self._normalize_vs_list(vs_list)
        logger.debug("Searching %d VS items for name=%s", len(items), target_name)
        for item in items:
            if item.get("name") == target_name:
                return item
        return None

    def pre_validation(self, vs_obj: Dict[str, Any]) -> bool:
        if not vs_obj:
            raise RuntimeError("Virtual Service not found")
        enabled = vs_obj.get("enabled")
        logger.info("Pre-Validation: VS %s enabled=%s", vs_obj.get("name"), enabled)
        if enabled is not True:
            raise RuntimeError("Virtual Service is not enabled; aborting")
        return True

    def task_trigger(self, vs_uuid: str) -> Dict[str, Any]:
        logger.info("Triggering PUT to disable VS uuid=%s", vs_uuid)
        resp = self.client.put_virtualservice(vs_uuid, {"enabled": False})
        logger.debug("PUT response body: %s", resp)
        return resp

    def post_validation(self, vs_uuid: str) -> Dict[str, Any]:
        logger.info("Post-validation GET for uuid=%s", vs_uuid)
        obj = self.client.get_virtualservice(vs_uuid)
        logger.info("Post-Validation: enabled=%s", obj.get("enabled"))
        return obj

    @_retry
    def pre_fetcher(self) -> Tuple[List[Dict[str, Any]], Any, Any]:
        tenants = self.client.list_tenants()
        vs_list = self.client.list_virtualservices()
        ses = self.client.list_serviceengines()
        logger.debug("Fetched tenants=%s vs_count=%s ses=%s", 
                     getattr(tenants, '__len__', lambda: None)(), 
                     getattr(vs_list, '__len__', lambda: None)(),
                     getattr(ses, '__len__', lambda: None)())
        return tenants, vs_list, ses

    def mock_ssh(self, host: str) -> bool:
        logger.debug("mock_ssh check to %s (stub)", host)
        return True

    def mock_rdp(self, host: str) -> bool:
        logger.debug("mock_rdp check to %s (stub)", host)
        return True

    def run_case(self, case_cfg: Dict[str, Any]) -> bool:
        name = case_cfg.get("name", "<unnamed>")
        target_name = case_cfg.get("target_vs_name") or self.cfg.get("target_vs_name")
        if not target_name:
            raise ValueError("target_vs_name must be provided in case_cfg or main config")

        logger.info("Running test case '%s' for VS '%s'", name, target_name)

        # Stage 1: fetch required resources
        try:
            tenants, vs_list, ses = self.pre_fetcher()
        except Exception as exc:
            logger.exception("Failed to pre-fetch API data for case %s: %s", name, exc)
            return False

        # Stage 2: find specific VS
        vs_obj = self.find_vs_by_name(vs_list, target_name)
        if not vs_obj:
            logger.error("Virtual Service named %s not found", target_name)
            return False

        try:
            self.pre_validation(vs_obj)
        except Exception as exc:
            logger.exception("Pre-validation failed for VS %s: %s", target_name, exc)
            return False

        try:
            self.mock_ssh(self.cfg.get("mock_ssh_host", "10.0.0.1"))
            self.mock_rdp(self.cfg.get("mock_rdp_host", "10.0.0.2"))
        except Exception as exc:
            logger.warning("Optional remote checks raised an exception (ignored): %s", exc)

        # Stage 3: task/trigger
        vs_uuid = vs_obj.get("uuid") or vs_obj.get("id") or vs_obj.get("name")
        if not vs_uuid:
            logger.error("VS object missing UUID/id/name; cannot proceed: %s", vs_obj)
            return False

        try:
            self.task_trigger(vs_uuid)
        except Exception as exc:
            logger.exception("Task trigger failed for uuid %s: %s", vs_uuid, exc)
            return False

        # Stage 4: post-validation
        try:
            post = self.post_validation(vs_uuid)
        except Exception as exc:
            logger.exception("Post-validation GET failed for uuid %s: %s", vs_uuid, exc)
            return False

        if post.get("enabled") is False:
            logger.info("Test PASS: VS %s disabled", target_name)
            return True
        else:
            logger.error("Test FAIL: VS %s still enabled after PUT", target_name)
            return False
