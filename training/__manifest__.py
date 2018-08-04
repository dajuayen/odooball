{
    'name': 'Training Sessions Directory',
    'category': 'Tools',
    'summary': 'Sessions, exercicies,...',
    'author': 'David Juaneda',
    'description': """
This module gives you a quick view of your planning directory with training sessions and exercices, 
accessible from your home page.
You can track your plans and trainig sessions.
""",
    'depends': ['players','project','document'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/training_views.xml',
    ],
    'installable': True,
}
