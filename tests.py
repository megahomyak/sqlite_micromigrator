import sqlite_micromigrator, sqlite3

class SuddenStop(Exception): pass

def migrate(log, cursor, do_sudden_stop=False, do_v2=True):
    migrator = sqlite_micromigrator.Migrator(cursor)
    @migrator
    def v0():
        log.append("v0")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS a (
            b TEXT,
            c TEXT
        );
        """)
    @migrator
    def v1():
        log.append("v1")
        sqlite_micromigrator.add_column(cursor, "a", "d", "BLOB")
        if do_sudden_stop:
            raise SuddenStop()
        sqlite_micromigrator.add_column(cursor, "a", "e", "BLOB")
    if do_v2:
        @migrator
        def v2():
            log.append("v2")
            sqlite_micromigrator.drop_column(cursor, "a", "d")
            sqlite_micromigrator.drop_column(cursor, "a", "e")

def main():
    def assert_equal(a, b):
        if a != b:
            raise AssertionError(f"{repr(a)} != {repr(b)}")
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        def assert_column_names(expected_column_names):
            cursor.execute(f"PRAGMA table_info(a);")
            actual_column_names = set(info_row[1] for info_row in cursor.fetchall())
            assert_equal(actual_column_names, expected_column_names)
        def check_migration(expected_log, expected_column_names, *args, **kwargs):
            log = []
            try:
                migrate(log, cursor, *args, **kwargs)
            except SuddenStop:
                pass
            cursor.execute(f"PRAGMA table_info(a);")
            column_names = set(info_row[1] for info_row in cursor.fetchall())
            assert_equal(log, expected_log)
            assert_equal(column_names, expected_column_names)
        check_migration(["v0", "v1"], {"b", "c", "d"}, do_sudden_stop=True)
        check_migration(["v1"], {"b", "c", "d", "e"}, do_v2=False)
        check_migration(["v2"], {"b", "c"})
        check_migration([], {"b", "c"})
        print("All tests passed")

main()
