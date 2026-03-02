# -*- coding: utf-8 -*-
from datetime import datetime
import pytz
from odoo import models, _

class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    def _get_prefix_suffix(self):
        """
        Generic implementation for Odoo 11-19 supporting %(uid)s
        """
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
            try:
                effective_date = datetime.strptime(self._context.get('ir_sequence_date'), '%Y-%m-%d')
            except (ValueError, TypeError): pass
        if self._context.get('ir_sequence_date_range'):
            try:
                range_date = datetime.strptime(self._context.get('ir_sequence_date_range'), '%Y-%m-%d')
            except (ValueError, TypeError): pass

        sequences = {
            'year': '%Y', 'month': '%m', 'day': '%d', 'y': '%y', 'doy': '%j', 'woy': '%W',
            'weekday': '%w', 'h24': '%H', 'h12': '%I', 'min': '%M', 'sec': '%S'
        }
        interpolation_dict = {}
        for key, fmt in sequences.items():
            interpolation_dict[key] = effective_date.strftime(fmt)
            interpolation_dict['range_' + key] = range_date.strftime(fmt)
            interpolation_dict['current_' + key] = now.strftime(fmt)

        interpolation_dict['uid'] = str(self.env.user.id)

        def _interpolate(value, data):
            return (value % data) if value else ''

        record = self[0]
        try:
            prefix = _interpolate(record.prefix, interpolation_dict)
            suffix = _interpolate(record.suffix, interpolation_dict)
        except (ValueError, KeyError, TypeError):
            return super(IrSequence, self)._get_prefix_suffix()

        return prefix, suffix
