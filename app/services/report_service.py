"""
Report Service
"""

from sqlalchemy.orm import Session

from app.models.report import Report


class ReportService:

    def __init__(self, db: Session):
        self.db = db


    def get_all_reports(self):
        return (
            self.db.query(Report)
            .all()
        )


    def get_report_by_id(
        self,
        report_id: str
    ):
        return (
            self.db.query(Report)
            .filter(
                Report.id == report_id
            )
            .first()
        )


    def create_report(
        self,
        report_data: dict
    ):
        report = Report(
            **report_data
        )

        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)

        return report


    def update_report(
        self,
        report_id: str,
        report_data: dict
    ):
        report = self.get_report_by_id(
            report_id
        )

        if not report:
            return None

        for key, value in report_data.items():
            setattr(
                report,
                key,
                value
            )

        self.db.commit()
        self.db.refresh(report)

        return report


    def delete_report(
        self,
        report_id: str
    ):
        report = self.get_report_by_id(
            report_id
        )

        if not report:
            return False

        self.db.delete(report)
        self.db.commit()

        return True