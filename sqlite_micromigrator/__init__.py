class Migrator:
    def __init__(self, cursor):
        self.cursor = cursor
        self.migrations_processed = 0
    def __call__(self, migration):
        self.cursor.execute("PRAGMA user_version;")
        current_version = self.cursor.fetchone()[0]
        if current_version == self.migrations_processed:
            migration()
            self.cursor.execute(f"PRAGMA user_version={current_version + 1};")
        self.migrations_processed += 1
        return migration

def add_column(cursor, table_name, column_name, column_type):
    cursor.execute(f"PRAGMA table_info({table_name});")
    column_names = [info_row[1] for info_row in cursor.fetchall()]
    if column_name not in column_names:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")

def drop_column(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    column_names = [info_row[1] for info_row in cursor.fetchall()]
    if column_name in column_names:
        cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name};")
