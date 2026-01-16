import argparse

from pathlib import Path

from storage.movie_storage import Movie
from storage.stream_storage import Stream
from storage.s3_client import S3Client
from storage.bucket import Bucket
from utils import *

S3_ENDPOINT_URL = "Please provide endpoint"

def parse_args():
    parser = argparse.ArgumentParser(
        description="Upload files to S3 with optional versioning and lifecycle rules"
    )

    # Required arguments
    parser.add_argument(
        "--dir-path",
        required=True,
        type=Path,
        help="Local directory containing files"
    )

    parser.add_argument(
        "--file-type",
        required=True,
        choices=["movie", "stream"],
        help="File type to process"
    )

    parser.add_argument(
        "--bucket-name",
        required=True,
        help="Target S3 bucket name. Must have at least 3 characters. May content . and -"
    )

    # Optional arguments
    parser.add_argument(
        "--prefix",
        default="",
        help="S3 key prefix"
    )

    parser.add_argument(
        "--versioning",
        action="store_true",
        help="Enable bucket versioning"
    )

    parser.add_argument(
        "--lifecycle",
        type=int,
        metavar="DAYS",
        help="Expire objects after N days"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if not args.dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {args.dir_path}")

    if args.file_type.lower() not in ['movie', 'stream']:
        raise ValueError("Unexpected file type")

    if len(args.bucket_name) < 3:
        raise ValueError("Bucket name is to short.")

    if args.lifecycle is not None and args.lifecycle <= 0:
        raise ValueError("lifecycle-days must be a positive integer")

    dir_path = args.dir_path
    file_type = args.file_type
    bucket_name = args.bucket_name
    prefix = args.prefix

    versioning = args.versioning
    lifecycle = args.lifecycle

    files=[]

    if file_type.lower() == 'movie':
        versioning = True
        files = [Movie(movie.name, movie) for movie in get_all_files_from_dir(dir_path)]

    elif file_type.lower() == 'stream':
        versioning = False
        files = [Stream(stream.name, stream) for stream in get_all_files_from_dir(dir_path)]

    print("S3 client connection")
    client = S3Client(endpoint_url=S3_ENDPOINT_URL)
    s3 = client.connect()

    print("Bucket creation")
    bucket = Bucket(bucket_name, s3)
    bucket.create()

    if versioning:
        bucket.set_versioning("Enabled")
    if lifecycle and not versioning:
        bucket.set_lifecycle("ScriptLifecycle", lifecycle)
    elif lifecycle and versioning:
        bucket.set_lifecycle("ScriptLifecycle", lifecycle, lifecycle)
    print("Uploading files:")
    for file in files:
        print(file.name)
        s3.upload_file(file.path, bucket_name, f"{prefix}{file.name}")

    if file_type.lower() == 'stream':
        meta_data = build_metadata(prefix=prefix, file_count=len(files))
        create_and_upload_json_data_file('meta', meta_data, s3, bucket_name, prefix=prefix)

        index_data = build_index(prefix=prefix, files=files)
        create_and_upload_json_data_file('index', index_data, s3, bucket_name, prefix=prefix)

    client.close()


if __name__ == "__main__":
    main()
