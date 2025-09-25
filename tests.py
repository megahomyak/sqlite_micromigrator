import sqlite_micromigrator

class SuddenInterruption(Exception): pass

def make_migrate_version(should_suddenly_interrupt, do_version_1):
    def migrate_version(version, cursor):
        if version == 0:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS a (
                b TEXT
            );
            """)
        elif version == 1 and do_version_1:
            sqlite_micromigrator.add_column("a", "c", "INTEGER")
            if should_suddenly_interrupt:
                raise SuddenInterruption()
            sqlite_micromigrator.add_column("a", "d", "BLOB")
        else:
            raise sqlite_micromigrator.MigrationNotFound()

def main():
    with sqlite3.connect("test.db") as conn:
        with conn.cursor() as cursor:
            sqlite_micromigrator.migrate(migrate_version, cursor)

main()
