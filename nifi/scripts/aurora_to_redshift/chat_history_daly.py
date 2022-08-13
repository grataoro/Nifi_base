import os

from migrations_lib import migrate


dirName = os.path.basename(__file__)

tableName = 'poli.new_chat_history'

select = \
"""
    SELECT id, customer_id, contact_id, origin_id, status, type, channel_id, attempts, redirected, redirected_to, department_id, closed_by, obs, closed_reason, score, count_messages, count_messages_user, first_reply, created_at, updated_at, finished_at, parent, last_message_time, started_conversation
    FROM chat_history
"""

tableNameWithSchema = "poli.new_chat_history (id, customer_id, contact_id, origin_id, status, type_, channel_id, attempts, redirected, redirected_to, department_id, closed_by, obs, closed_reason, score, count_messages, count_messages_user, first_reply, created_at, updated_at, finished_at, parent, last_message_time, started_conversation)"


migration = migrate(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName,
                                    daly=True)

print(migration)

