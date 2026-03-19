{
    'name': 'Custom Attendance',
    'version': '1.0',
    'summary': 'Module chấm công',
    'author': 'SSM company',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/attendance_report_views.xml',
        'views/attendance_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_attendance/static/src/js/geolocation_widget.js',
        ],
    },
    'installable': True,
    'application': True,
}
