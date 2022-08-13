import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.customer_cred_payments'

select = """
    SELECT id, customer_cred_id, invoice_id_sl, date_payment, contact_quantity, release_manual_contact_day, release_user_id_by, release_manual_date, value_payment, created_at, updated_at, status_payment, link_invoice, due_date, date_ref 
    FROM  customer_cred_payments
"""

tableNameWithSchema = "poli.customer_cred_payments (id, customer_cred_id, invoice_id_sl, date_payment, contact_quantity, release_manual_contact_day, release_user_id_by, release_manual_date, value_payment, created_at, updated_at, status_payment, link_invoice, due_date, date_ref)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)

