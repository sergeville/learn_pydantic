from __future__ import annotations

from studentdb_tools import DatabaseDeps, get_student_balance, get_student_profile, money


if __name__ == "__main__":
    deps = DatabaseDeps()
    profile = get_student_profile(deps, "0001005")
    balance = get_student_balance(deps, "0001005")

    if not profile:
        raise SystemExit("Student not found")

    print("Pydantic model:")
    print(profile.model_dump_json(indent=2))

    print("\nBeginner-friendly answer:")
    print(
        f"{profile.display_name} is in {profile.plan} with GPA {profile.gpa}. "
        f"FERPA flag is {profile.ferpa_flag}."
    )
    if balance:
        print(f"Balance for term {balance.term}: {money(balance.balance)}")
