# Copyright 2018 David Juaneda - <djuaneda@sdi.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class PlayerPositionTag(models.Model):
    _description = 'Position Tags'
    _name = 'res.partner.position'
    _order = 'parent_left, name'
    _parent_store = True
    _parent_order = 'name'

    name = fields.Char(string='Position Name', required=True, translate=True)
    color = fields.Integer(string='Color Index')
    parent_id = fields.Many2one('res.partner.position', string='Parent Position Tag', index=True, ondelete='cascade')
    child_ids = fields.One2many('res.partner.position', 'parent_id', string='Child Position Tag')
    active = fields.Boolean(default=True, help="The active field allows you to hide the position without removing it.")
    parent_left = fields.Integer(string='Left parent', index=True)
    parent_right = fields.Integer(string='Right parent', index=True)
    partner_ids = fields.Many2many('res.partner', column1='position_tag', column2='partner_id', string='Partners')
    description = fields.Text(string='Description position')

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You can not create recursive tags.'))

    @api.multi
    def name_get(self):
        """ Return the products' display name, including their direct
            parent by default.

            If ``context['partner_product_display']`` is ``'short'``, the short
            version of the position name (without the direct parent) is used.
            The default is the long version.
        """
        if self._context.get('player_function_display') == 'short':
            return super(PlayerPositionTag, self).name_get()

        res = []
        for position in self:
            names = []
            current = position
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((position.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self.search(args, limit=limit).name_get()


class Partner(models.Model):
    _inherit = 'res.partner'

    def _default_position_tag(self):
        return self.env['res.partner.position'].browse(self._context.get('position_tag'))

    member_type = fields.Selection(string='Member Type',
                                    selection=[('player', 'Player'),
                                               ('coach', 'Coach'),
                                               ('responsible', 'Responsible')],)
    team_id = fields.Many2one('res.team', string='Team')
    position_tag = fields.Many2many('res.partner.position', column1='partner_id',
                                   column2='position_tag', string='Position', default=_default_position_tag)
