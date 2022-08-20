echo "---------------------------------"
echo "------Creando Nuevo Modulo-------"
echo "---------------------------------"

echo "Ingrese el nombre del Modulo: "
read NAME

mkdir $NAME

mkdir $NAME/controllers
echo -e "# -*- coding: utf-8 -*- \n
from . import controllers" >> $NAME/controllers/__init__.py

echo -e "# -*- coding: utf-8 -*-
# from odoo import http


# class ${NAME}(http.Controller):
#     @http.route('/${NAME}/${NAME}/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/${NAME}/${NAME}/', auth='public')
#     def list(self, **kw):
#         return http.request.render('${NAME}.listing', {
#             'root': '/${NAME}/${NAME}/',
#             'objects': http.request.env['${NAME}.${NAME}'].search([]),
#         })

#     @http.route('/${NAME}/${NAME}/objects/<model("${NAME}.${NAME}"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('${NAME}.object', {
#             'object': obj
#         })
" >> $NAME/controllers/controllers.py
mkdir $NAME/demo
echo -e "<odoo>
    <data>

    </data>
</odoo>" >> $NAME/demo/demo.xml

mkdir $NAME/models
echo -e "# -*- coding: utf-8 -*- \n
from . import models" >> $NAME/models/__init__.py
echo -e "# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ${NAME}(models.Model):
#     _name = '${NAME}.${NAME}'
#     _description = '${NAME}.${NAME}'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
" >> $NAME/models/models.py
mkdir $NAME/security
echo -e "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_${NAME}_${NAME},${NAME}.${NAME},model_${NAME}_${NAME},base.group_user,1,1,1,1
" >> $NAME/security/ir.model.access.csv
mkdir $NAME/static
mkdir $NAME/static/src
mkdir $NAME/views
echo -e "<odoo>
    <data>
      
    </data>
</odoo>" >> $NAME/views/templates.xml

echo -e "<odoo>
  <data>
    
  </data>
</odoo>" >> $NAME/views/views.xml

echo -e "# -*- coding: utf-8 -*-\n
from . import controllers
from . import models
" > $NAME/__init__.py

echo -e "# -*- coding: utf-8 -*-
{
    'name': '${NAME}',

    'summary': '',

    'description': '',

    'author': 'VMC Solutions',
    'website': 'http://www.yourcompany.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}" > $NAME/__manifest__.py