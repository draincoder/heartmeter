from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker

from diary.application.interfaces import ReportPublisher
from diary.infrastructure.rmq.publisher import RMQReportPublisher


class RMQProvider(Provider):
    def __init__(self, broker: RabbitBroker) -> None:
        super().__init__()
        self._broker = broker

    @provide(scope=Scope.APP)
    def get_report_publisher(self) -> ReportPublisher:
        return RMQReportPublisher(self._broker.publisher())
