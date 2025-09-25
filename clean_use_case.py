import sqlite_micromigrator, sqlite3

def migrate(cursor):
    migrator = sqlite_micromigrator.Migrator(cursor)
    @migrator
    def v0():
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS a (
            b TEXT,
            c TEXT
        );
        """)
    @migrator
    def v1():
        sqlite_micromigrator.add_column(cursor, "a", "d", "BLOB")
        sqlite_micromigrator.add_column(cursor, "a", "e", "BLOB")
    @migrator
    def v2():
        sqlite_micromigrator.drop_column(cursor, "a", "d")
        sqlite_micromigrator.drop_column(cursor, "a", "e")

def main():
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        migrate(cursor)
        # ...rest of app code...

main()
