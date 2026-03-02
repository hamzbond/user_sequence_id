# -*- coding: utf-8 -*-

from datetime import datetime

import pytz

from odoo import api, models, _
from odoo.exceptions import UserError


class UserIdService(object):

    def __init__(self, env):
        self.env = env

    def get_current_uid(self):
        user = self.env.user
        if user:
            return str(user.id)
        return ''


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    @api.multi
    def _get_prefix_suffix(self):
        uses_custom_legend = any(
            '%(uid)s' in (rec.prefix or '') or '%(uid)s' in (rec.suffix or '')
            for rec in self
        )
        if not uses_custom_legend:
            return super(IrSequence, self)._get_prefix_suffix()

        now = range_date = effective_date = datetime.now(
            pytz.timezone(self._context.get('tz') or 'UTC')
        )
        if self._context.get('ir_sequence_date'):
            effective_date = datetime.strptime(self._context.get('ir_sequence_date'), '%Y-%m-%d')
        if self._context.get('ir_sequence_date_range'):
            range_date = datetime.strptime(self._context.get('ir_sequence_date_range'), '%Y-%m-%d')

        sequences = {
            'year': '%Y', 'month': '%m', 'day': '%d', 'y': '%y', 'doy': '%j', 'woy': '%W',
            'weekday': '%w', 'h24': '%H', 'h12': '%I', 'min': '%M', 'sec': '%S'
        }
        interpolation_dict = {}
        for key, fmt in sequences.items():
            interpolation_dict[key] = effective_date.strftime(fmt)
            interpolation_dict['range_' + key] = range_date.strftime(fmt)
            interpolation_dict['current_' + key] = now.strftime(fmt)

        interpolation_dict['uid'] = UserIdService(self.env).get_current_uid()

        def _interpolate(value, data):
            return (value % data) if value else ''

        record = self[0]
        try:
            prefix = _interpolate(record.prefix, interpolation_dict)
            suffix = _interpolate(record.suffix, interpolation_dict)
        except ValueError:
            raise UserError(_('Invalid prefix or suffix for sequence "%s"') % (record.name,))

        return prefix, suffix
