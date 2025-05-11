from datetime import date
from io import BytesIO

from openpyxl.workbook import Workbook
from opentelemetry import trace

from reporter.application.dto import Report, Weather
from reporter.application.interfaces import ReportGenerator
from reporter.domain.models import Measurement

tracer = trace.get_tracer(__name__)


class ExcelGenerator(ReportGenerator):
    @tracer.start_as_current_span("excel generation")
    def generate(self, data: list[Measurement], weathers: dict[date, Weather]) -> Report:
        wb = Workbook()
        ws = wb.active
        ws.title = "Health Report"
        ws.append(["Date", "Systolic", "Diastolic", "Pulse", "Drug", "Note", "Temperature", "Pressure"])

        data.sort(key=lambda d: d.date)
        for m in data:
            weather = weathers[m.date.date()]
            ws.append(
                [
                    m.date.strftime("%Y-%m-%d %H:%M"),
                    m.systolic,
                    m.diastolic,
                    m.pulse,
                    m.drug,
                    m.note,
                    weather.temperature,
                    weather.pressure,
                ]
            )

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        filename = f"{data[0].date.strftime('%Y_%m_%d')}_{data[-1].date.strftime('%Y_%m_%d')}.xlsx"
        return Report(payload=output.read(), format="xlsx", filename=filename)
