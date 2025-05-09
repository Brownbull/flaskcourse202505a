# init
$ flask shell
>>> db.create_all()

# insert
$ flask shell
>>> from app import insert_data
>>> insert_data()

# query
$ flask shell
>>> from app import query_data
>>> query_data()

# update
>>> from app import update_data_by_id
>>> update_data_by_id(1)
Data updated successfully!
>>> update_data_by_id(2)
User not found.

# delete
>>> from app import delete_data_by_id
>>> delete_data_by_id(1)
Data deleted successfully!
>>> delete_data_by_id(2)
User not found.

# one to many
## do changes then
$ flask shell
>>> db.create_all()