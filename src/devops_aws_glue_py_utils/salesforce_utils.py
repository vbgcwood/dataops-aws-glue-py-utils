# salesforce_utils.py
from .validation_utils import verify_sanitized
from .logging_utils import setup_logger

logger = setup_logger(__name__)


def build_secure_soql_query(
    entity: str, extract_fields: list[str], /, ignore_ids: list[str] = []
) -> str:
    """
    Builds an SOQL query that extracts fields whiles excluding specific IDs
    while verifying input is sanitized.

    Parameters:
    - entity (str): The name of the salesforce object to extract.
    - extract_fields (list[str]): List of fields to extract.
    - ignore_ids (list[str]): List of IDs to exclude.

    Returns:
    - str: The generated SOQL query.
    """
    if ignore_ids and not extract_fields:
        raise ValueError("You must provide fields to extract when excluding IDs.")

    verify_sanitized(entity)
    verify_sanitized(extract_fields)
    verify_sanitized(ignore_ids)

    fields_str = ",".join(extract_fields)
    ids_str = "','".join(ignore_ids)
    query = f"SELECT {fields_str} FROM {entity} WHERE Id NOT IN ('{ids_str}')"
    return query


def get_salesforce_obj_as_dynamic_frame(
    glue_context,
    connection_name: str,
    api_version: str,
    entity: str,
    /,
    extract_fields: list[str] = [],
    ignore_ids: list[str] = []
):
    """
    Retrieves a Salesforce object as a DynamicFrame while verifying input is sanitized.

    Parameters:
    - glue_context (glue_context): The glue_context object.
    - connection_name (str): The name of the connection in the Glue Data Catalog.
    - api_version (str): The Salesforce API version.
    - entity (str): The name of the Salesforce object to extract.

    Key Arguments:
    - extract_fields (list[str]): List of fields to extract.
    - ignore_ids (list[str]): List of IDs to exclude.

    Returns:
    - DynamicFrame: The Salesforce object as a DynamicFrame.
    """
    connection_options = {
        "connectionName": connection_name,
        "API_VERSION": api_version,
        "ENTITY_NAME": entity,
    }

    if extract_fields and not ignore_ids:
        connection_options["SELECT_FIELDS"] = extract_fields
    elif ignore_ids:
        # Builds a query while verifying input is sanitized
        query = build_secure_soql_query(entity, extract_fields, ignore_ids)
        if query:
            connection_options["QUERY"] = query
            logger.warning(f"Entity using custom query: {entity}; Query: {query}")

    dynamic_frame = glue_context.create_dynamic_frame.from_options(
        connection_type="salesforce",
        connection_options=connection_options,
        transformation_ctx=f"Salesforce_{entity}",
    )

    return dynamic_frame


def save_dynamic_frame_to_s3(
    glue_context, dynamic_frame, save_path: str, save_format: str
):
    """
    Save a DynamicFrame to an S3 bucket by path.

    Parameters:
    - glue_context (glue_context): The glue_context object.
    - dynamic_frame: The DynamicFrame to save.
    - save_path (str): The S3 path to save the DynamicFrame.
    - save_format (str): The format to save the DynamicFrame in.

    Returns:
    - None
    """
    glue_context.write_dynamic_frame.from_options(
        frame=dynamic_frame,
        connection_type="s3",
        connection_options={"path": save_path},
        format=save_format,
    )
