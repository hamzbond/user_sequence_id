{
    'name': 'User ID in Sequence Legend',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': 'Add current User ID to sequence prefix or suffix using %(uid)s',
    'description': """
This module extends the Odoo sequence functionality to allow using the current user's ID as a dynamic placeholder in prefixes and suffixes.

Key Features:
-------------
* Adds support for `%(uid)s` in any sequence definition.
* Returns the ID of the user who is currently performing the action.
* Compatible with standard Odoo sequence legends (year, month, day, etc.).
* Lightweight and safe: falls back to default Odoo behavior if placeholder is not used.

Usage:
------
1. Go to Settings > Technical > Sequences & Identifiers > Sequences.
2. Edit a sequence (e.g., Sales Order).
3. Add `%(uid)s` to the Prefix or Suffix field.
4. The placeholder will be replaced by the numeric User ID in the generated number.
    """,
    'author': 'hamzbond',
    'website': 'https://hamzbond.github.io',
    'license': 'LGPL-3',
    'support': 'hamzbond@gmail.com',
    'images': ['static/description/banner.png'],
    'depends': ['base'],
    'data': [
        'views/ir_sequence_views.xml',
    ],
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
