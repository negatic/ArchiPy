import logging
from typing import override

from confluent_kafka import Consumer, KafkaError, Message, Producer, TopicPartition
from confluent_kafka.admin import AdminClient, ClusterMetadata, NewTopic

from archipy.adapters.kafka.ports import KafkaAdminPort, KafkaConsumerPort, KafkaProducerPort
from archipy.configs.base_config import BaseConfig
from archipy.configs.config_template import KafkaConfig
from archipy.models.errors.custom_errors import (
    InternalError,
    InvalidArgumentError,
    UnavailableError,
)
from archipy.models.types.language_type import LanguageType

logger = logging.getLogger(__name__)


class KafkaAdminAdapter(KafkaAdminPort):
    """Synchronous Kafka admin adapter."""

    def __init__(self, kafka_configs: KafkaConfig | None = None) -> None:
        """Initialize the admin adapter with Kafka configuration.

        Args:
            kafka_configs: Optional Kafka configuration. If None, uses global config.
        """
        configs: KafkaConfig = kafka_configs or BaseConfig.global_config().KAFKA
        try:
            broker_list_csv = ",".join(configs.BROKERS_LIST)
            config = {"bootstrap.servers": broker_list_csv}
            if configs.USER_NAME and configs.PASSWORD and configs.CERT_PEM:
                config |= {
                    "sasl.username": configs.USER_NAME,
                    "sasl.password": configs.PASSWORD,
                    "security.protocol": configs.SECURITY_PROTOCOL,
                    "sasl.mechanisms": configs.SASL_MECHANISMS,
                    "ssl.endpoint.identification.algorithm": "none",
                    "ssl.ca.pem": configs.CERT_PEM,
                }
            self.adapter: AdminClient = AdminClient(config)
        except Exception as e:
            raise InternalError(details=str(e), lang=LanguageType.FA) from e

    @override
    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        """Create a new Kafka topic.

        Args:
            topic: Name of the topic to create
            num_partitions: Number of partitions for the topic
            replication_factor: Replication factor for the topic
        """
        try:
            new_topic = NewTopic(topic, num_partitions, replication_factor)
            self.adapter.create_topics([new_topic])
            logger.debug(
                f"Created topic {topic} with {num_partitions} partitions and replication factor {replication_factor}",
            )
        except Exception as e:
            raise InternalError(details=f"Failed to create topic {topic}", lang=LanguageType.FA) from e

    @override
    def delete_topic(self, topics: list[str]) -> None:
        """Delete one or more Kafka topics."""
        try:
            self.adapter.delete_topics(topics)
            logger.debug("Deleted topics", topics)
        except Exception as e:
            raise InternalError(details="Failed to delete topics", lang=LanguageType.FA) from e

    @override
    def list_topics(
        self,
        topic: str | None = None,
        timeout: int = 1,
    ) -> ClusterMetadata:
        """List Kafka topics."""
        try:
            return self.adapter.list_topics(topic=topic, timeout=timeout)
        except Exception as e:
            raise UnavailableError(service="Kafka", lang=LanguageType.FA) from e


class KafkaConsumerAdapter(KafkaConsumerPort):
    """Synchronous Kafka consumer adapter."""

    def __init__(
        self,
        group_id: str,
        topic_list: list[str] | None = None,
        partition_list: list[TopicPartition] | None = None,
        kafka_configs: KafkaConfig | None = None,
    ) -> None:
        """Initialize with Kafka configuration and subscription.

        Args:
            group_id: Consumer group ID.
            topic_list: List of topics to subscribe to.
            partition_list: List of partitions to assign.
            kafka_configs: Optional Kafka configuration.
        """
        configs: KafkaConfig = kafka_configs or BaseConfig.global_config().KAFKA
        self._adapter: Consumer = self._get_adapter(group_id, configs)
        if topic_list and not partition_list:
            self.subscribe(topic_list)
        elif not topic_list and partition_list:
            self.assign(partition_list)
        else:
            logger.error("Invalid topic or partition list")
            raise InvalidArgumentError(
                argument_name="topic_list or partition_list",
                lang=LanguageType.FA,
            )

    @staticmethod
    def _get_adapter(group_id: str, configs: KafkaConfig) -> Consumer:
        """Create and configure Consumer."""
        try:
            broker_list_csv = ",".join(configs.BROKERS_LIST)
            config = {
                "bootstrap.servers": broker_list_csv,
                "group.id": group_id,
                "session.timeout.ms": configs.SESSION_TIMEOUT_MS,
                "auto.offset.reset": configs.AUTO_OFFSET_RESET,
                "enable.auto.commit": configs.ENABLE_AUTO_COMMIT,
            }
            if configs.USER_NAME and configs.PASSWORD and configs.CERT_PEM:
                config |= {
                    "sasl.username": configs.USER_NAME,
                    "sasl.password": configs.PASSWORD,
                    "security.protocol": configs.SECURITY_PROTOCOL,
                    "sasl.mechanisms": configs.SASL_MECHANISMS,
                    "ssl.endpoint.identification.algorithm": "none",
                    "ssl.ca.pem": configs.CERT_PEM,
                }
            return Consumer(config)
        except Exception as e:
            raise InternalError(details=str(e), lang=LanguageType.FA) from e

    @override
    def batch_consume(self, messages_number: int = 500, timeout: int = 1) -> list[Message]:
        """Consume a batch of messages."""
        try:
            result_list: list[Message] = []
            messages: list[Message] = self._adapter.consume(num_messages=messages_number, timeout=timeout)
            for message in messages:
                if message.error():
                    logger.error("Consumer error", message.error())
                    continue
                logger.debug("Message consumed", message)
                message.set_value(message.value())
                result_list.append(message)
                self.commit(message, asynchronous=True)
            else:
                return result_list
        except Exception as e:
            raise InternalError(details="Failed to consume batch", lang=LanguageType.FA) from e

    @override
    def poll(self, timeout: int = 1) -> Message | None:
        """Poll for a single message."""
        try:
            message: Message | None = self._adapter.poll(timeout)
            if message is None:
                logger.debug("No message received")
                return None
            if message.error():
                logger.error("Consumer error", message.error())
                return None
            logger.debug("Message consumed", message)
            message.set_value(message.value())
        except Exception as e:
            raise InternalError(details="Failed to poll message", lang=LanguageType.FA) from e
        else:
            return message

    @override
    def commit(self, message: Message, asynchronous: bool = True) -> None | list[TopicPartition]:
        """Commit message offset."""
        try:
            return self._adapter.commit(message=message, asynchronous=asynchronous)
        except Exception as e:
            raise InternalError(details="Failed to commit message", lang=LanguageType.FA) from e

    @override
    def subscribe(self, topic_list: list[str]) -> None:
        """Subscribe to topics."""
        try:
            self._adapter.subscribe(topic_list)
            logger.debug("Subscribed to topics", topic_list)
        except Exception as e:
            raise InternalError(
                details="Failed to subscribe to topics",
                lang=LanguageType.FA,
            ) from e

    @override
    def assign(self, partition_list: list[TopicPartition]) -> None:
        """Assign partitions."""
        try:
            self._adapter.assign(partition_list)
            for partition in partition_list:
                self._adapter.seek(partition)
            logger.debug("Assigned partitions", partition_list)
        except Exception as e:
            raise InternalError(
                details="Failed to assign partitions",
                lang=LanguageType.FA,
            ) from e


class KafkaProducerAdapter(KafkaProducerPort):
    """Synchronous Kafka producer adapter."""

    def __init__(self, topic_name: str, kafka_configs: KafkaConfig | None = None) -> None:
        """Initialize with Kafka configuration and topic.

        Args:
            topic_name: Topic to produce to.
            kafka_configs: Optional Kafka configuration.
        """
        configs: KafkaConfig = kafka_configs or BaseConfig.global_config().KAFKA
        self.topic = topic_name
        self._adapter: Producer = self._get_adapter(configs)

    @staticmethod
    def _get_adapter(configs: KafkaConfig) -> Producer:
        """Create and configure Producer."""
        try:
            broker_list_csv = ",".join(configs.BROKERS_LIST)
            config = {
                "bootstrap.servers": broker_list_csv,
                "queue.buffering.max.ms": configs.MAX_BUFFER_MS,
                "queue.buffering.max.messages": configs.MAX_BUFFER_SIZE,
                "acks": configs.ACKNOWLEDGE_COUNT,
                "request.timeout.ms": configs.REQUEST_ACK_TIMEOUT_MS,
                "delivery.timeout.ms": configs.DELIVERY_MESSAGE_TIMEOUT_MS,
            }
            if configs.USER_NAME and configs.PASSWORD and configs.CERT_PEM:
                config |= {
                    "sasl.username": configs.USER_NAME,
                    "sasl.password": configs.PASSWORD,
                    "security.protocol": configs.SECURITY_PROTOCOL,
                    "sasl.mechanisms": configs.SASL_MECHANISMS,
                    "ssl.endpoint.identification.algorithm": "none",
                    "ssl.ca.pem": configs.CERT_PEM,
                }
            return Producer(config)
        except Exception as e:
            raise InternalError(details=str(e), lang=LanguageType.FA) from e

    @staticmethod
    def _pre_process_message(message: str | bytes) -> bytes:
        """Convert message to bytes."""
        return message if isinstance(message, bytes) else message.encode("utf-8")

    @staticmethod
    def _delivery_callback(error: KafkaError | None, message: Message) -> None:
        """Handle delivery result."""
        if error:
            logger.error("Message failed delivery", error)
            logger.debug("Message = %s", message)
            raise InternalError(
                details="Message failed delivery",
                lang=LanguageType.FA,
            )
        logger.debug("Message delivered", message)

    @override
    def produce(self, message: str | bytes) -> None:
        """Produce a message to a topic."""
        try:
            processed_message = self._pre_process_message(message)
            self._adapter.produce(self.topic, processed_message, on_delivery=self._delivery_callback)
        except Exception as e:
            raise InternalError(
                details="Failed to produce message",
                lang=LanguageType.FA,
            ) from e

    @override
    def flush(self, timeout: int | None = None) -> None:
        """Flush pending messages."""
        try:
            self._adapter.flush(timeout=timeout)
        except Exception as e:
            raise InternalError(
                details="Failed to flush messages",
                lang=LanguageType.FA,
            ) from e

    @override
    def validate_healthiness(self) -> None:
        """Validate producer health."""
        try:
            self.list_topics(self.topic, timeout=1)
        except Exception as e:
            raise UnavailableError(
                service="Kafka",
                lang=LanguageType.FA,
            ) from e

    @override
    def list_topics(
        self,
        topic: str | None = None,
        timeout: int = 1,
    ) -> ClusterMetadata:
        """List Kafka topics."""
        try:
            topic = topic or self.topic
            return self._adapter.list_topics(topic=topic, timeout=timeout)
        except Exception as e:
            raise UnavailableError(
                service="Kafka",
                lang=LanguageType.FA,
            ) from e
