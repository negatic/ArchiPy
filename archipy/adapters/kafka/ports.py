from abc import abstractmethod

from confluent_kafka import Message, TopicPartition
from confluent_kafka.admin import ClusterMetadata


class KafkaAdminPort:
    """Interface for Kafka admin operations."""

    @abstractmethod
    def delete_topic(self, topics: list[str]) -> None:
        """Delete one or more Kafka topics."""
        raise NotImplementedError

    @abstractmethod
    def list_topics(self, topic: str | None = None, timeout: int = 1) -> ClusterMetadata:
        """List Kafka topics."""
        raise NotImplementedError


class KafkaConsumerPort:
    """Interface for Kafka consumer operations."""

    @abstractmethod
    def batch_consume(self, messages_number: int, timeout: int) -> list[Message]:
        """Consume a batch of messages."""
        raise NotImplementedError

    @abstractmethod
    def poll(self, timeout: int) -> Message | None:
        """Poll for a single message."""
        raise NotImplementedError

    @abstractmethod
    def commit(self, message: Message, asynchronous: bool) -> None | list[TopicPartition]:
        """Commit message offset."""
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, topic_list: list[str]) -> None:
        """Subscribe to topics."""
        raise NotImplementedError

    @abstractmethod
    def assign(self, partition_list: list[TopicPartition]) -> None:
        """Assign partitions."""
        raise NotImplementedError


class KafkaProducerPort:
    """Interface for Kafka producer operations."""

    @abstractmethod
    def produce(self, message: str | bytes) -> None:
        """Produce a message to a topic."""
        raise NotImplementedError

    @abstractmethod
    def flush(self, timeout: int | None) -> None:
        """Flush pending messages."""
        raise NotImplementedError

    @abstractmethod
    def validate_healthiness(self) -> None:
        """Validate producer health."""
        raise NotImplementedError

    @abstractmethod
    def list_topics(self, topic: str | None, timeout: int) -> ClusterMetadata:
        """List Kafka topics."""
        raise NotImplementedError
