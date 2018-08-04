# Copyright 2018 David Juaneda - <juayen@hotmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _


class Users(models.Model):
    _inherit = "res.users"

    team_ids = fields.Many2many('res.team', 'res_team_users_rel', 'user_id', 'team_id', string=_('My teams'))
