# stuff done by db.sh
# 01
$ sqlite3 db.sqlite3
$ .tables
$ .exit
# 02 create class Member
$ flask db init
$ flask db migrate
$ flask db upgrade
# 03 create class Order
$ flask db migrate
$ flask db upgrade
# 04 downdgrade
$ flask db downgrade
