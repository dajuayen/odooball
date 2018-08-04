# Copyright 2018 David Juaneda - <juayen@hotmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource
from odoo.exceptions import ValidationError, UserError


class ResField(models.Model):
    _description = 'Football field'
    _name = "res.field"
    _order = "name"

    name = fields.Char('Name', translate=True)
    full_name = fields.Char('Full Name', translate=True)
    active = fields.Boolean('Active', default=True)
    description = fields.Text(string="", required=False,
                              help='Small description of the field.')
    surface = fields.Selection(string="Surface",
                             selection=[('natual', 'Natural'),
                                        ('artificial', 'Artificial')],
                             required=False)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    phone = fields.Char(help="Phone of field.")
    email = fields.Char(help="Email of field.")
    website = fields.Char(help="Website of field.")

    team_ids = fields.One2many('res.team', 'field_id', string='Teams', help='Teams play in this field.')
    comment = fields.Text(string='Notes')

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary("Image", attachment=True,
        help="This field holds the image used as avatar for this team, limited to 1024x1024px",)
    image_medium = fields.Binary("Medium-sized image", attachment=True,
        help="Medium-sized image of this team. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved. "\
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
        help=_("Small-sized image of this team. It is automatically "\
             "resized as a 64x64px image, with aspect ratio preserved. "\
             "Use this field anywhere a small image is required."))
