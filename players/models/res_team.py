# Copyright 2018 David Juaneda - <djuaneda@sdi.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
import os
import threading

from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource
from odoo.exceptions import ValidationError, UserError


class Team(models.Model):
    _name = "res.team"
    _description = 'Teams'
    _order = 'sequence, name'

    def _get_logo(self):
        return base64.b64encode(open(os.path.join(tools.config['root_path'], 'addons', 'base', 'res', 'res_company_logo.png'), 'rb') .read())

    @api.model
    def _get_euro(self):
        return self.env['res.currency.rate'].search([('rate', '=', 1)], limit=1).currency_id

    @api.model
    def _get_user_currency(self):
        currency_id = self.env['res.users'].browse(self._uid).company_id.currency_id
        return currency_id or self._get_euro()

    name = fields.Char(string='Team Name', compute='_compute_team_name')
    club_id = fields.Many2one('res.team.club', 'Club')
    category_id = fields.Many2one('res.team.category', 'Category')
    season_id = fields.Many2one('res.team.season', 'Season')
    sequence = fields.Integer(help='Used to order Teams in the team switcher', default=10)
    # image: all image fields are base64 encoded and PIL-supported
    gadge = fields.Binary("Image", attachment=True,
        help="This field holds the image used as avatar for this team, limited to 1024x1024px",)
    gadge_medium = fields.Binary("Medium-sized image", attachment=True,
        help="Medium-sized image of this team. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved. "\
             "Use this field in form views or some kanban views.")
    gadge_small = fields.Binary("Small-sized image", attachment=True,
        help="Small-sized image of this team. It is automatically "\
             "resized as a 64x64px image, with aspect ratio preserved. "\
             "Use this field anywhere a small image is required.")

    user_ids = fields.Many2many('res.users', 'res_company_users_rel', 'cid', 'user_id', string='Accepted Users')

    email = fields.Char(help="Email of Team, person responsible or manager.")
    phone = fields.Char(help="Phone of Team, person responsible or manager.")
    website = fields.Char(help="Website of Team, person responsible or manager.")

    player_ids = fields.One2many('res.partner', 'team_id', string='Players', help='Players related to this team.')

    comment = fields.Text(string='Notes')

    @api.multi
    @api.onchange('club_id', 'category_id', 'season_id')
    def _compute_team_name(self):
        for team in self:
            team.name = ''
            if team.club_id:
                team.name = team.name + team.club_id.name
            if team.category_id:
                if team.name == '':
                    team.name = team.category_id.name_first_parent()
                else:
                    team.name = " - "\
                        .join([team.name,
                               team.category_id.name_first_parent()])
            if team.season_id:
                if team.name == '':
                    team.name = team.season_id.name
                else:
                    team.name = " - ".join([team.name, team.season_id.name])


    @api.model
    def _get_default_image(self, partner_type, is_company, parent_id):
        if getattr(threading.currentThread(), 'testing', False) \
            or self._context.get('install_mode'):
            return False

        colorize, img_path, image = False, False, False

        if partner_type in ['other'] and parent_id:
            parent_image = self.browse(parent_id).image
            image = parent_image and base64.b64decode(parent_image) or None

        if not image and partner_type == 'invoice':
            img_path = get_module_resource('base', 'static/src/img', 'money.png')
        elif not image and partner_type == 'delivery':
            img_path = get_module_resource('base', 'static/src/img', 'truck.png')
        elif not image and is_company:
            img_path = get_module_resource('base', 'static/src/img', 'company_image.png')
        elif not image:
            img_path = get_module_resource('base', 'static/src/img', 'avatar.png')
            colorize = True

        if img_path:
            with open(img_path, 'rb') as f:
                image = f.read()
        if image and colorize:
            image = tools.image_colorize(image)

        return tools.image_resize_image_big(base64.b64encode(image))


class TeamClub(models.Model):
    _description = 'Club'
    _name = "res.team.club"
    _order = "name"

    name = fields.Char('Name', translate=True)
    full_name = fields.Char('Full Name', translate=True)
    active = fields.Boolean('Active', default=True)


class Season(models.Model):
    _description = 'Season'
    _name = "res.team.season"
    _order = "name"

    name = fields.Char('Name', translate=True)
    full_name = fields.Char('Full Name', translate=True)
    active = fields.Boolean('Active', default=True)


class TeamCategory(models.Model):
    _description = 'Category'
    _name = "res.team.category"
    _order = 'parent_left, name'
    _parent_store = True
    _parent_order = 'name'

    name = fields.Char(string='Position Name', required=True, translate=True)
    color = fields.Integer(string='Color Index')
    parent_id = fields.Many2one('res.team.category', string='Parent Position Tag', index=True, ondelete='cascade')
    child_ids = fields.One2many('res.team.category', 'parent_id', string='Child Position Tag')
    active = fields.Boolean(default=True, help="The active field allows you to hide the category without removing it.")
    parent_left = fields.Integer(string='Left parent', index=True)
    parent_right = fields.Integer(string='Right parent', index=True)
    teams_ids = fields.One2many('res.team', 'category_id', string='Teams')
    description = fields.Text(string='Description category')

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You can not create recursive tags.'))

    @api.multi
    def name_first_parent(self):
        for category in self:
            if category.parent_id:
                parent = category.parent_id
                while parent.parent_id:
                    parent = parent.parent_id
                return parent.name
            else:
                return category.name

    @api.multi
    def name_get(self):
        """ Return the products' display name, including their direct
            parent by default.

            If ``context['partner_product_display']`` is ``'short'``, the short
            version of the position name (without the direct parent) is used.
            The default is the long version.
        """
        if self._context.get('team_category_display') == 'short':
            return super(TeamCategory, self).name_get()

        res = []
        for category in self:
            names = []
            current = category
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((category.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self.search(args, limit=limit).name_get()
