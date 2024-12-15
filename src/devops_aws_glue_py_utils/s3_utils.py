# s3_utils.py
from itertools import islice
from typing import Callable, Iterable, Generator


def batch_iterable(iterable: Iterable[any], size: int) -> Generator[list[any]]:
    """
    Yield successive batches of a specified size from an iterable.

    Parameters:
    - iterable (Iterable): Any iterable object.
    - size (int): Size of each batch.

    Returns:
    - Generator: A generator that yields batches of the specified size.
    """
    it = iter(iterable)
    while True:
        current_batch = list(islice(it, size))
        if not current_batch:
            break
        yield current_batch


def truncate_s3_entire_path(
    s3_client,
    bucket_name: str,
    prefix: str = "",
    batch_size: int = 1000,
    /,
    response_hook: Callable = None
) -> None:
    """
    Deletes all objects in an S3 bucket with a specified prefix.

    Parameters:
    - s3_client: A boto3 S3 client.
    - bucket_name: The buck name to connect to.
    - prefix (int): The prefix to delete. Will recursively delete all objects with this prefix.
    - batch_size (int): The number of objects to delete in each batch.

    Key Arguments:
    - response_hook (Callable): A function to handle the responses from the S3 API.

    Returns:
    - None
    """
    paginator = s3_client.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        if "Contents" in page:
            delete_keys = [{"Key": obj["Key"]} for obj in page["Contents"]]

            for batch in batch_iterable(delete_keys, batch_size):
                response = s3_client.delete_objects(
                    Bucket=bucket_name, Delete={"Objects": batch}
                )
                if response_hook:
                    response_hook(response)
