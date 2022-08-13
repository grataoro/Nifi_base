import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.departments'

select = """
    SELECT  *
    FROM departments
"""

tableNameWithSchema = "poli.departments (id, type, customer_id, key, screening_id, name, label, status, default_, created_at, updated_at, deleted_at, revsync)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)
