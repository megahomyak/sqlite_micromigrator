def add_column(cursor, table_name, column_name, column_type):
    cursor.execute(f"PRAGMA table_info({table_name});")
    column_names = [info_row[1] for info_row in cursor.fetchall()]
    if column_name not in column_names:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")

def remove_column(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    column_names = [info_row[1] for info_row in cursor.fetchall()]
    if column_name in column_names:
        cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name};")

class MigrationNotFound(Exception): pass

def migrate(migrate_version, cursor):
    def get_database_version(cursor):
        c.execute("PRAGMA user_version;")
        return c.fetchone()[0]
    def set_database_version(cursor, new_version):
        c.execute(f"PRAGMA user_version={new_version};")
    try:
        while True:
            current_version = get_database_version(cursor)
            migrate_version(current_version, cursor)
            set_database_version(current_version + 1, cursor)
    except MigrationNotFound:
        pass
