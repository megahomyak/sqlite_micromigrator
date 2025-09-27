This is a super tiny SQLite database migrator, aimed to be used in the tiniest scripts to allow them to be production-ready while remaining straightforward, simple and understandable.

Migrations done with this migrator, given they're done idempotently, can be stopped at any point. There are helper functions - `add_column` and `drop_column` - that help making adding and removing columns idempotent. Idempotent table creation can be done using `CREATE TABLE IF NOT EXISTS`, and idempotent table dropping can be done using `DROP TABLE IF EXISTS`.

# Usage

Before your main code, write this to be executed once:

```
import sqlite3, sqlite_micromigrator
conn = sqlite3.connect("...your path...")
cursor = conn.cursor()
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
```

That's all you need. No need to call anything to "apply migrations" - they're being applied as they're being declared. After all of the migrations are declared, just start using the database as if it was on the latest declared migration.

**Rollbacks are not yet supported.** I have no plans to add them, but I may, later.
