import sqlite_micromigrator, sqlite3

class SuddenStop(Exception): pass

def make_migrate_version(log, do_sudden_stop=False, version_bound=None):
    def migrate_version(cursor, version):
        if version_bound is not None and version >= version_bound:
            raise sqlite_micromigrator.MigrationNotFound()
        if version == 0:
            log.append("v0")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS a (
                b TEXT,
                c TEXT
            );
            """)
        elif version == 1:
            log.append("v1")
            sqlite_micromigrator.add_column(cursor, "a", "d", "BLOB")
            if do_sudden_stop:
                raise SuddenStop()
            sqlite_micromigrator.add_column(cursor, "a", "e", "BLOB")
        elif version == 2:
            log.append("v2")
            sqlite_micromigrator.drop_column(cursor, "a", "d")
            sqlite_micromigrator.drop_column(cursor, "a", "e")
        else:
            raise sqlite_micromigrator.MigrationNotFound()
    return migrate_version

def main():
    log = []
    def assert_equal(a, b):
        try:
            assert a == b
        except AssertionError:
            print(a, b)
            raise
    def assert_and_clear_log(expected_log):
        assert_equal(log, expected_log)
        log.clear()
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        def assert_column_names(expected_column_names):
            cursor.execute(f"PRAGMA table_info(a);")
            actual_column_names = set(info_row[1] for info_row in cursor.fetchall())
            assert_equal(actual_column_names, expected_column_names)
        try:
            sqlite_micromigrator.migrate(cursor, make_migrate_version(log, do_sudden_stop=True))
        except SuddenStop:
            pass
        assert_and_clear_log(["v0", "v1"])
        assert_column_names({"b", "c", "d"})
        sqlite_micromigrator.migrate(cursor, make_migrate_version(log, version_bound=2))
        assert_and_clear_log(["v1"])
        assert_column_names({"b", "c", "d", "e"})
        sqlite_micromigrator.migrate(cursor, make_migrate_version(log))
        assert_and_clear_log(["v2"])
        assert_column_names({"b", "c"})
        sqlite_micromigrator.migrate(cursor, make_migrate_version(log, do_sudden_stop=False))
        assert_and_clear_log([])
        assert_column_names({"b", "c"})
        print("All tests passed")

main()
