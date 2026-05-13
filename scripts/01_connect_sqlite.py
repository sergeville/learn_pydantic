from __future__ import annotations

from studentdb_tools import DatabaseDeps, fetch_all, list_database_objects


def sample_profiles(deps: DatabaseDeps) -> list[dict]:
    return fetch_all(
        deps,
        """
        SELECT
          EMPLID,
          DISPLAY_NAME,
          FERPA_FLAG,
          PROG_DESCR,
          PLAN_DESCR,
          CUM_GPA,
          PROG_STATUS
        FROM V_STUDENT_360
        ORDER BY EMPLID
        LIMIT 5
        """,
    )


if __name__ == "__main__":
    deps = DatabaseDeps()
    print("Database:", deps.db_path)

    print("\nTables and views:")
    for row in list_database_objects(deps):
        print(f"- {row['type']}: {row['name']}")

    print("\nSample V_STUDENT_360 rows:")
    for row in sample_profiles(deps):
        print(row)
