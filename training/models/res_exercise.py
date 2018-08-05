# Copyright 2018 David Juaneda - <juayen@hotmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields, _

class Exercise(models.Model):
    _name = "res.exercise"
    _description = "Exercise"
    _inherit = "project.task"
    _order = "date_start"

    project_id = fields.Many2one('res.training',
                                 string='Training session',
                                 default=lambda self: self.env.context.get('default_training_id'),
                                 index=True,
                                 track_visibility='onchange',
                                 change_default=True)
