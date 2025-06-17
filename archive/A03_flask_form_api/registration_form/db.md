# init
$ flask shell
>>> from registration_form import create_app
>>> from registration_form.extensions import db
>>> from registration_form.models import member_topic_table, Member, Language, Topic
>>> db.create_all()
>>> from app import *

# insert
$ flask shell
>>> from registration_form import create_app
>>> from registration_form.extensions import db
>>> from registration_form.models import Language, Topic
>>> python = Language(name='Python')
>>> javascript = Language(name='Javascript')
>>> php = Language(name='PHP')
>>> ruby = Language(name='Ruby')
>>> c = Language(name='C')
>>> go = Language(name='Go')
>>> web_apps = Topic(name='Web Apps')
>>> mobile_apps = Topic(name='Mobile Apps')
>>> api = Topic(name='APIs')
>>> app = create_app()
>>> app.app_context().push()
>>> db.session.add_all([python, javascript, php, ruby, c, go])
>>> db.session.add_all([web_apps, mobile_apps, api])
>>> db.session.commit()

