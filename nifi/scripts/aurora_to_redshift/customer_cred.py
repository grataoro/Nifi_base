import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)


tableName = 'poli.customer_cred'

select = \
"""
    SELECT id, customer_id, package_quantity, contact_quantity, value, "type", status, date_of_next_recurrent, service_id, created_at, updated_at, due_date_plan, installment 
    FROM customer_cred
"""

tableNameWithSchema = "poli.customer_cred (id, customer_id, package_quantity, contact_quantity, value, type, status, date_of_next_recurrent, service_id, created_at, updated_at, due_date_plan, installment)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)

