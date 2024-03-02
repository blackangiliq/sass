# -*- coding: utf-8 -*-
{
    'name': "Nat Sass Management",
    'sequence': -100,  # هنا الترتيب مالتة بداخل قائمة التطبيقات لسهولة الوصول الة وتحديثة اثناء التطوير
    'application': True,  # نوعة للتطبيق ابلكيشن مو مودل
    'category': 'Accounting/Accounting',  # نوعيتة بداخل العرض التصنيفي الي ع اليسار من تدخلون ع التطبيقات
    'author': "mohammed essa",  # اسم الناشر للتطبيق عند التنصيب
    'version': '0.1',
    'depends': ['base'],
    # في جالة جان اكو تطبيق ثاني يعتمد علي التطبيق هذا الي جاي نشتغل علي على قاعدة بياناتنة فيتصنب اثناء تنصيب هذا المودل

    'data': [
        # 'security/ir.model.access.csv',
        'security/sas_security_profile.xml',
        'views/sass_admin_account.xml',
        'views/users_profile_type.xml',
        'views/users.xml',
        'views/inventory.xml',
        'views/inventory_employee.xml',

        'views/task_proplem_type.xml',
        'views/user_expier_whatsapp_msaage.xml',
        'views/task.xml',
        'views/task_attachmeint.xml',
        'views/task_change_user_info_request.xml',
        'views/users_expire_soon.xml',
        'views/rc.xml',
        'views/dp.xml',
        'data/inital_models_value_on_install.xml',
        'views/root_menu.xml',

    ],
    'assets': {
        'web.assets_backend': [
            # 'sass/static/src/js/list_view_button.js',

        ]
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
