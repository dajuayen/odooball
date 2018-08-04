# Copyright 2018 David Juaneda - <juayen@hotmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields, _

class Training(models.Model):
    _name = "res.training"
    _description = "Training"
    _inherit = "project.project"
    _order = "date_start"

    date_start = fields.Date(string=_('Start Training'), index=True, track_visibility='onchange')
    date = fields.Date(string='Session finish')
    team_id = fields.Many2one('res.team', required=True,
                              # domain=[('uid', 'in', 'user_ids')],
                              # context="{'uid': self.env.user.id}"
                              )
    field_id = fields.Many2one('res.field', string=_("Training ground"))
