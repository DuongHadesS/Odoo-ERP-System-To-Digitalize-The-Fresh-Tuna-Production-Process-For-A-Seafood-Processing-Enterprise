from odoo import models, fields, api
from datetime import datetime

class CustomAttendance(models.Model):
    _name = "custom.attendance"
    _description = "Custom Attendance"

    employee_id = fields.Many2one("hr.employee", string="Nhân viên", required=True)
    check_in = fields.Datetime(string="Giờ vào")
    check_out = fields.Datetime(string="Giờ ra")
    worked_hours = fields.Float(string="Số giờ làm", compute="_compute_worked_hours", store=True)
    state = fields.Selection([
        ("checked_in", "Đang làm việc"),
        ("checked_out", "Đã kết thúc"),
    ], string="Trạng thái", default="checked_out")


    latitude = fields.Float(string='Vĩ độ', digits=(16, 7))
    longitude = fields.Float(string='Kinh độ', digits=(16, 7))
    map_embed = fields.Html("Map Embed", compute="_compute_map_embed", sanitize=False)


    @api.depends("check_in", "check_out")
    def _compute_worked_hours(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                delta = rec.check_out - rec.check_in
                rec.worked_hours = delta.total_seconds() / 3600.0
            else:
                rec.worked_hours = 0.0
            if rec.worked_hours > 8:
                rec.worked_hours = 8.0

    def action_check_in(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'get_location',
            'target': 'new',
            'params': {
                'model': self._name,
                'resId': self.ids[0] if self.ids else False,
                'employee_id': self.employee_id.id if self.employee_id else False,
                'mode': 'check_in',
            },
        }

    def action_check_in_with_coords(self, lat=None, lng=None):
        for rec in self:
            rec.write({
                "check_in": fields.Datetime.now(),
                "state": "checked_in",
                "check_out": False,
                "worked_hours": 0.0,
                "latitude": lat,
                "longitude": lng,
            })
        return True

    def action_check_out(self, lat=None, lng=None):
        for rec in self:
            if rec.check_in:
                vals = {
                    "check_out": fields.Datetime.now(),
                    "state": "checked_out",
                }
                if lat is not None and lng is not None:
                    vals.update({"latitude": lat, "longitude": lng})
                rec.write(vals) 

    def action_open_map(self):
        for rec in self:
            if rec.latitude and rec.longitude:
                map_url = f"https://www.google.com/maps?q={rec.latitude},{rec.longitude}"
                return {
                    'type': 'ir.actions.act_url',
                    'url': map_url,
                    'target': 'new',
                }
            else:
                # Trường hợp chưa có tọa độ
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Thông báo',
                        'message': 'Chưa có vị trí để mở bản đồ!',
                        'sticky': False,
                    }
                }
            
    @api.depends("latitude", "longitude")
    def _compute_map_embed(self):
        for rec in self:
            if rec.latitude and rec.longitude:
                rec.map_embed = f"""
                    <iframe 
                        src="https://www.google.com/maps?q={rec.latitude},{rec.longitude}&hl=vi&z=16&output=embed" 
                        width="100%" height="300" style="border:0;" allowfullscreen>
                    </iframe>
                """
            else:
                rec.map_embed = "<p style='color:gray'>Chưa có dữ liệu vị trí</p>"
