# Copyright 2018 David Juaneda - <juayen@hotmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools, _

class Team(models.Model):
    _inherit = "res.team"

    training_ids = fields.One2many("res.training", "team_id", string="Training Sessions",
                                   required=False,
                                   help=_('Training sessions related to this team.'))
