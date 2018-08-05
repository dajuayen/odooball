# Copyright 2018 David Juaneda - <juayen@hotmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields, _

class Training(models.Model):
    _name = "res.training"
    _inherit = ['project.project']
    _description = "Training"
    _order = "date_start"

    date_start = fields.Date(string=_('Start Training'), index=True, track_visibility='onchange')
    date = fields.Date(string='Session finish')
    team_id = fields.Many2one('res.team', required=True,
                              # domain=[('uid', 'in', 'user_ids')],
                              # context="{'uid': self.env.user.id}"
                              )
    field_id = fields.Many2one('res.field', string=_("Training ground"))

    @api.multi
    def attachment_tree_view(self):
        self.ensure_one()
        domain = [
            '|',
            '&', ('res_model', '=', 'res.training'), ('res_id', 'in', self.ids),
            '&', ('res_model', '=', 'res.execise'), ('res_id', 'in', self.task_ids.ids)]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                            Documents are attached to the tasks and issues of your project.</p><p>
                            Send messages or log internal notes with attachments to link
                            documents to your project.
                        </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }

        def _compute_task_count(self):
            task_data = self.env['res.exercise'].read_group(
                [('training_id', 'in', self.ids), '|', ('stage_id.fold', '=', False), ('stage_id', '=', False)],
                ['training_id'], ['training_id'])
            result = dict((data['project_id'][0], data['project_id_count']) for data in task_data)
            for trainig in self:
                trainig.task_count = result.get(trainig.id, 0)
