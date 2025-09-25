import sqlite_micromigrator, sqlite3

def migrate_version(cursor, version):
    if version == 0:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS a (
            b TEXT,
            c TEXT
        );
        """)
    elif version == 1:
        sqlite_micromigrator.add_column(cursor, "a", "d", "BLOB")
        sqlite_micromigrator.add_column(cursor, "a", "e", "BLOB")
    elif version == 2:
        sqlite_micromigrator.drop_column(cursor, "a", "d")
        sqlite_micromigrator.drop_column(cursor, "a", "e")
    else:
        raise sqlite_micromigrator.MigrationNotFound()

def main():
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        sqlite_micromigrator.migrate(cursor, migrate_version)
        # ...rest of app logic...

main()
