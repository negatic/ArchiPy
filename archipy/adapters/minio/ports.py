"""MinIO port definitions for ArchiPy."""

from abc import abstractmethod
from typing import Any, BinaryIO

# Define type aliases for better type hinting
MinioObjectType = dict[str, Any]
MinioBucketType = dict[str, Any]
MinioPolicyType = dict[str, Any]


class MinioPort:
    """Interface for MinIO operations providing a standardized access pattern.

    This interface defines the contract for MinIO adapters, ensuring consistent
    implementation of object storage operations across different adapters.
    """

    # Bucket Operations
    @abstractmethod
    def bucket_exists(self, bucket_name: str) -> bool:
        """Check if a bucket exists."""
        raise NotImplementedError

    @abstractmethod
    def make_bucket(self, bucket_name: str) -> None:
        """Create a new bucket."""
        raise NotImplementedError

    @abstractmethod
    def remove_bucket(self, bucket_name: str) -> None:
        """Remove a bucket."""
        raise NotImplementedError

    @abstractmethod
    def list_buckets(self) -> list[MinioBucketType]:
        """List all buckets."""
        raise NotImplementedError

    # Object Operations
    @abstractmethod
    def put_object(self, bucket_name: str, object_name: str, file_path: str) -> None:
        """Upload a file to a bucket."""
        raise NotImplementedError

    @abstractmethod
    def get_object(self, bucket_name: str, object_name: str, file_path: str) -> None:
        """Download an object to a file."""
        raise NotImplementedError

    @abstractmethod
    def remove_object(self, bucket_name: str, object_name: str) -> None:
        """Remove an object from a bucket."""
        raise NotImplementedError

    @abstractmethod
    def list_objects(
        self,
        bucket_name: str,
        prefix: str = "",
        *,  # Force recursive to be keyword-only to avoid boolean flag issues
        recursive: bool = False,
    ) -> list[MinioObjectType]:
        """List objects in a bucket.

        Args:
            bucket_name: The name of the bucket to list objects from
            prefix: Optional prefix to filter objects by
            recursive: Whether to list objects recursively (include sub-directories)

        Returns:
            A list of MinioObjectType objects
        """
        raise NotImplementedError

    @abstractmethod
    def stat_object(self, bucket_name: str, object_name: str) -> MinioObjectType:
        """Get object metadata."""
        raise NotImplementedError

    # Presigned URL Operations
    @abstractmethod
    def presigned_get_object(self, bucket_name: str, object_name: str, expires: int = 3600) -> str:
        """Generate a presigned URL for downloading an object."""
        raise NotImplementedError

    @abstractmethod
    def presigned_put_object(self, bucket_name: str, object_name: str, expires: int = 3600) -> str:
        """Generate a presigned URL for uploading an object."""
        raise NotImplementedError

    # Policy Operations
    @abstractmethod
    def set_bucket_policy(self, bucket_name: str, policy: str) -> None:
        """Set bucket policy."""
        raise NotImplementedError

    @abstractmethod
    def get_bucket_policy(self, bucket_name: str) -> MinioPolicyType:
        """Get bucket policy."""
        raise NotImplementedError

    @abstractmethod
    def copy_object(
        self,
        src_bucket_name: str,
        src_object_name: str,
        dest_bucket_name: str,
        dest_object_name: str,
    ) -> None:
        """Copy an object within or between buckets."""
        raise NotImplementedError

    @abstractmethod
    def put_object_stream(
        self,
        bucket_name: str,
        object_name: str,
        data: bytes | BinaryIO,
        length: int = -1,
        content_type: str = "application/octet-stream",
    ) -> None:
        """Upload data from a bytes buffer or binary stream to a bucket.

        Unlike put_object which requires a local file path, this method accepts
        in-memory bytes or any binary stream, avoiding the need for a temporary file.

        Args:
            bucket_name: Destination bucket name.
            object_name: Object name in the bucket.
            data: Content to upload as raw bytes or a binary stream (BinaryIO).
            length: Content length in bytes. If -1, computed automatically for bytes;
                for streams, providing the exact length avoids buffering overhead.
            content_type: MIME type of the content. Defaults to "application/octet-stream".
        """
        raise NotImplementedError

    @abstractmethod
    def get_object_stream(self, bucket_name: str, object_name: str) -> bytes:
        """Download an object and return its content as bytes.

        Unlike get_object which requires a local file path, this method returns
        the object content directly in memory, avoiding a temporary file.

        Args:
            bucket_name: Source bucket name.
            object_name: Object name in the bucket.

        Returns:
            bytes: The full content of the object.
        """
        raise NotImplementedError
