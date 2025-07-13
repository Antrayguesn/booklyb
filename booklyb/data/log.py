import logging

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format="")

INFO_RUN_STRATEGY = "INFO_0001"
INFO_LOADING_DATA = "INFO_0002"
INFO_PROCESSING_DATA = "INFO_0003"
INFO_WRITING_DATA = "INFO_0004"
INFO_END_PROCESS = "INFO_0005"

INFO_RUN_STRATEGIES = "INFO_0007"

WARNING_UNEXECPT_ERROR = "WARNING_0001"
WARNING_NO_CENTROID = "WARNING_0002"


def log(code, msg, service_code=None, **kwargs):
    severity = code.split("_")[0]
    json_log = {"CODE": code, "MSG": msg, "SEVERITY": severity, "SERVICE_CODE": service_code, **kwargs}
    if severity == "INFO":
        logger.info(json_log)
    elif severity == "DEBUG":
        logger.debug(json_log)
    elif severity == "ERROR":
        logger.error(json_log)
    elif severity == "WARNING":
        logger.warning(json_log)
