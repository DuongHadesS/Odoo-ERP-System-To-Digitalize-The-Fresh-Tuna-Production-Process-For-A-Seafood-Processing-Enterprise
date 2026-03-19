from odoo import models, fields, api
from datetime import timedelta

class AttendanceReport(models.Model):
    _name = "attendance.report"
    _description = "Báo cáo chấm công"
    _auto = False   # dùng SQL view, không tạo bảng thực

    employee_id = fields.Many2one("hr.employee", string="Nhân viên")
    date = fields.Date("Ngày")
    worked_hours = fields.Float("Giờ đã làm")
    planned_hours = fields.Float("Giờ dự kiến")
    difference = fields.Float("Chênh lệch")
    balance = fields.Float("Số dư")


    

    @api.model
    def init(self):
        # Xóa view cũ nếu có
        self._cr.execute("""DROP VIEW IF EXISTS attendance_report""")
        # Tạo view mới
        self._cr.execute("""
            CREATE or REPLACE VIEW attendance_report AS (
                SELECT
                    MIN(a.id) as id,
                    a.employee_id as employee_id,
                    DATE(a.check_in) as date,
                    SUM(a.worked_hours) as worked_hours,
                    8.0 as planned_hours,
                    SUM(a.worked_hours) - 8.0 as difference,
                    SUM(a.worked_hours) - 8.0 as balance
                FROM custom_attendance a
                GROUP BY a.employee_id, DATE(a.check_in)
            )
        """)
