import os
from typing import Dict
import sys
from .logger import setup_logger

logger = setup_logger(__name__)


def determine_env() -> Dict[str, any]:
    """
    Determine the execution environment (Glue or Local) and extract job details if applicable.

    Returns:
        dict: A dictionary with the following keys:
            - 'glue' (bool): True if running in AWS Glue, False otherwise.
            - 'local' (bool): True if running locally, False otherwise.
            - 'job_name' (str or None): The name of the Glue job, if available.
    """
    env = {"glue": False, "local": False, "job_name": None}

    # Check for AWS Glue-specific environment variables
    if "AWS_EXECUTION_ENV" in os.environ or "GLUE_SCRIPT_PATH" in os.environ:
        env["glue"] = True

        try:
            from awsglue.utils import getResolvedOptions

            args = getResolvedOptions(sys.argv, ["JOB_NAME"])
            env["job_name"] = args.get("JOB_NAME")
        except ImportError:
            logger.warning(
                "Unable to import AWS Glue libraries. Job name not determined."
            )
        except KeyError:
            logger.warning(f"JOB_NAME not found with getResolvedOptions")
    else:
        env["local"] = True

    return env
