from . import models

def uninstall_hook(cr, registry):
    cr.execute("""
        UPDATE ir_sequence
        SET prefix = REPLACE(prefix, '%(uid)s', ''),
            suffix = REPLACE(suffix, '%(uid)s', '')
        WHERE prefix LIKE '%%(uid)s%%' OR suffix LIKE '%%(uid)s%%'
    """)