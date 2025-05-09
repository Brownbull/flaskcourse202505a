# init
$ flask shell
>>> db.create_all()

# insert
$ flask shell
>>> from app import insert_data
>>> insert_data()

# update
>>> from app import update_data_by_id
>>> update_data_by_id(1)
Data updated successfully!
>>> update_data_by_id(2)
User not found.

