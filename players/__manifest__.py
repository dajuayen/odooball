{
    'name': 'Players Directory',
    'category': 'Tools',
    'summary': 'Coachs, Partners,...',
    'author': 'David Juaneda',
    'description': """
This module gives you a quick view of your contacts directory, accessible from your home page.
You can track your players and other contacts.
""",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/player_views.xml',
        'views/position_tag_views.xml',
        'views/res_field_views.xml',
        'views/res_partner_views.xml',
        'views/res_team_category_views.xml',
        'views/res_team_club_views.xml',
        'views/res_team_season_views.xml',
        'views/res_team_views.xml',
    ],
    'installable': True,
}
