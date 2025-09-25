class Migrator:
    def __init__(self):
        self.migrations = []
    def register(self, migration):
        self.migrations.append(migration)
        return migration
    def migrate(self, cursor):
        while True:
            cursor.execute("PRAGMA user_version;")
            current_version = cursor.fetchone()[0]
            try:
                migration = self.migrations[current_version]
            except IndexError:
                break
            migration()
            cursor.execute(f"PRAGMA user_version={current_version + 1};")

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
