from __future__ import annotations

from studentdb_tools import (
    DatabaseDeps,
    find_students_with_holds,
    find_students_with_positive_balance,
    get_student_balance,
    get_student_classes,
    get_student_holds,
    get_student_profile,
    money,
)


if __name__ == "__main__":
    deps = DatabaseDeps()
    emplid = "0001006"

    print("Profile:")
    print(get_student_profile(deps, emplid))

    print("\nClasses:")
    for student_class in get_student_classes(deps, emplid):
        print(student_class)

    print("\nBalance:")
    balance = get_student_balance(deps, emplid)
    print(money(balance.balance) if balance else "No balance listed")

    print("\nHolds for student:")
    for hold in get_student_holds(deps, emplid):
        print(hold)

    print("\nAll students with holds:")
    for hold in find_students_with_holds(deps):
        print(f"{hold.display_name}: {hold.code} / {hold.reason}")

    print("\nStudents with positive balances:")
    for row in find_students_with_positive_balance(deps):
        print(f"{row.display_name}: {money(row.balance)}")
