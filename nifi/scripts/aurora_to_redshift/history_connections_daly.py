import os

from migrations_lib import migrate


dirName = os.path.basename(__file__)

tableName = 'public.history_connections'

select = \
"""
    SELECT id, channel_id, status_before, status_after, duration, created_at, updated_at
    FROM history_connections
"""

tableNameWithSchema = "public.history_connections (id, channel_id, status_before, status_after, duration, created_at, updated_at)"

migration = migrate(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName,
                                    daly=True)

print(migration)

