from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


COURSE_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = COURSE_ROOT / "data" / "student_mock.db"


@dataclass
class DatabaseDeps:
    db_path: Path = DB_PATH
    oprid: str = dataclass_field(default_factory=lambda: os.getenv("STUDENTDB_OPRID", "REGISTRAR_ALL").upper())


class AccessDenied(BaseModel):
    oprid: str
    emplid: str
    message: str


class StudentProfile(BaseModel):
    emplid: str
    display_name: str
    ferpa_flag: str
    academic_career: str | None = None
    program_code: str | None = None
    program: str | None = None
    plan_code: str | None = None
    plan: str | None = None
    program_status: str | None = None
    gpa: float | None = None
    cumulative_units: int | None = None
    term: str | None = None
    term_description: str | None = None
    enrollment_status: str | None = None


class StudentClass(BaseModel):
    emplid: str
    display_name: str
    term: str
    class_number: str
    subject: str
    catalog_number: str
    course: str
    enrollment_status: str
    units: int
    grade: str | None = None


class StudentBalance(BaseModel):
    emplid: str
    display_name: str
    term: str
    balance: float


class StudentHold(BaseModel):
    emplid: str
    display_name: str
    code: str
    reason: str
    start_term: str | None = None
    impact: str


class ChecklistItem(BaseModel):
    emplid: str
    display_name: str
    checklist: str
    item: str
    description: str
    status: str
    due_date: str | None = None
    admin_function: str | None = None


class StudentRequirement(BaseModel):
    emplid: str
    display_name: str
    plan: str
    requirement_group: str
    requirement: str
    status: str
    units_required: int
    units_completed: int


class FinancialAidAward(BaseModel):
    emplid: str
    aid_year: str
    institution: str
    item_type: str
    award: str
    award_status: str
    offer_amount: int
    accept_amount: int
    disbursement_status: str


class StudentSuccessReport(BaseModel):
    profile: StudentProfile | None
    classes: list[StudentClass]
    balance: StudentBalance | None
    holds: list[StudentHold]
    checklists: list[ChecklistItem]
    incomplete_requirements: list[StudentRequirement]
    financial_aid: list[FinancialAidAward] = Field(default_factory=list)


def fetch_all(deps: DatabaseDeps, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    connection = sqlite3.connect(deps.db_path)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(sql, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def list_database_objects(deps: DatabaseDeps) -> list[dict[str, Any]]:
    return fetch_all(
        deps,
        """
        SELECT name, type
        FROM sqlite_master
        WHERE type IN ('table', 'view')
        ORDER BY type, name
        """,
    )


def get_operator_access(deps: DatabaseDeps) -> dict[str, Any]:
    rows = fetch_all(
        deps,
        """
        SELECT OPRID, DESCR, ACCESS_PROFILE
        FROM PS_SCRTY_OPR
        WHERE OPRID = ?
        """,
        (deps.oprid,),
    )
    allowed = fetch_all(
        deps,
        """
        SELECT EMPLID, DISPLAY_NAME, FERPA_FLAG, ACCESS_REASON
        FROM V_ROW_SECURITY_ACCESS
        WHERE OPRID = ?
          AND EMPLID IS NOT NULL
        ORDER BY EMPLID
        """,
        (deps.oprid,),
    )
    return {
        "operator": rows[0] if rows else None,
        "allowed_students": allowed,
        "allowed_count": len(allowed),
    }


def can_access_student(deps: DatabaseDeps, emplid: str) -> bool:
    rows = fetch_all(
        deps,
        """
        SELECT 1
        FROM PS_SCRTY_STUDENT
        WHERE OPRID = ?
          AND EMPLID = ?
        LIMIT 1
        """,
        (deps.oprid, emplid),
    )
    return bool(rows)


def find_students(deps: DatabaseDeps, text: str) -> list[dict[str, Any]]:
    return fetch_all(
        deps,
        """
        SELECT p.EMPLID, p.DISPLAY_NAME, p.FERPA_FLAG
        FROM CS_CC_PERSON p
        JOIN PS_SCRTY_STUDENT sec
          ON sec.EMPLID = p.EMPLID
         AND sec.OPRID = ?
        WHERE p.EMPLID = ?
           OR lower(p.DISPLAY_NAME) LIKE '%' || lower(?) || '%'
        ORDER BY p.EMPLID
        LIMIT 10
        """,
        (deps.oprid, text, text),
    )


def get_student_profile(deps: DatabaseDeps, emplid: str) -> StudentProfile | None:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          DISPLAY_NAME AS display_name,
          FERPA_FLAG AS ferpa_flag,
          ACAD_CAREER AS academic_career,
          ACAD_PROG AS program_code,
          PROG_DESCR AS program,
          ACAD_PLAN AS plan_code,
          PLAN_DESCR AS plan,
          PROG_STATUS AS program_status,
          CUM_GPA AS gpa,
          TOT_CUMULATIVE AS cumulative_units,
          STRM AS term,
          TERM_DESCR AS term_description,
          ENROLL_STATUS AS enrollment_status
        FROM V_STUDENT_360
        WHERE EMPLID = ?
          AND EXISTS (
            SELECT 1 FROM PS_SCRTY_STUDENT sec
            WHERE sec.OPRID = ?
              AND sec.EMPLID = V_STUDENT_360.EMPLID
          )
        """,
        (emplid, deps.oprid),
    )
    return StudentProfile(**rows[0]) if rows else None


def get_student_classes(deps: DatabaseDeps, emplid: str) -> list[StudentClass]:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          DISPLAY_NAME AS display_name,
          STRM AS term,
          CLASS_NBR AS class_number,
          SUBJECT AS subject,
          CATALOG_NBR AS catalog_number,
          COURSE_DESCR AS course,
          ENRL_STATUS AS enrollment_status,
          UNITS_TAKEN AS units,
          NULLIF(CRSE_GRADE_OFF, '') AS grade
        FROM V_STUDENT_CLASSES
        WHERE EMPLID = ?
          AND EXISTS (
            SELECT 1 FROM PS_SCRTY_STUDENT sec
            WHERE sec.OPRID = ?
              AND sec.EMPLID = V_STUDENT_CLASSES.EMPLID
          )
        ORDER BY STRM, SUBJECT, CATALOG_NBR
        """,
        (emplid, deps.oprid),
    )
    return [StudentClass(**row) for row in rows]


def get_student_balance(deps: DatabaseDeps, emplid: str) -> StudentBalance | None:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          DISPLAY_NAME AS display_name,
          STRM AS term,
          BALANCE AS balance
        FROM V_STUDENT_BALANCE
        WHERE EMPLID = ?
          AND EXISTS (
            SELECT 1 FROM PS_SCRTY_STUDENT sec
            WHERE sec.OPRID = ?
              AND sec.EMPLID = V_STUDENT_BALANCE.EMPLID
          )
        """,
        (emplid, deps.oprid),
    )
    return StudentBalance(**rows[0]) if rows else None


def get_student_holds(deps: DatabaseDeps, emplid: str) -> list[StudentHold]:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          DISPLAY_NAME AS display_name,
          SRVC_IND_CD AS code,
          SRVC_IND_REASON AS reason,
          START_TERM AS start_term,
          IMPACT AS impact
        FROM V_STUDENT_HOLDS
        WHERE EMPLID = ?
          AND EXISTS (
            SELECT 1 FROM PS_SCRTY_STUDENT sec
            WHERE sec.OPRID = ?
              AND sec.EMPLID = V_STUDENT_HOLDS.EMPLID
          )
        ORDER BY SRVC_IND_CD
        """,
        (emplid, deps.oprid),
    )
    return [StudentHold(**row) for row in rows]


def get_student_checklists(deps: DatabaseDeps, emplid: str) -> list[ChecklistItem]:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          DISPLAY_NAME AS display_name,
          CHECKLIST_CD AS checklist,
          CHECKLIST_ITEM_CD AS item,
          ITEM_DESCR AS description,
          STATUS AS status,
          DUE_DT AS due_date,
          ADMIN_FUNCTION AS admin_function
        FROM V_STUDENT_CHECKLISTS
        WHERE EMPLID = ?
          AND EXISTS (
            SELECT 1 FROM PS_SCRTY_STUDENT sec
            WHERE sec.OPRID = ?
              AND sec.EMPLID = V_STUDENT_CHECKLISTS.EMPLID
          )
        ORDER BY DUE_DT, CHECKLIST_CD, CHECKLIST_ITEM_CD
        """,
        (emplid, deps.oprid),
    )
    return [ChecklistItem(**row) for row in rows]


def get_student_requirements(deps: DatabaseDeps, emplid: str) -> list[StudentRequirement]:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          DISPLAY_NAME AS display_name,
          ACAD_PLAN AS plan,
          RQRMNT_GROUP AS requirement_group,
          RQRMNT_DESCR AS requirement,
          STATUS AS status,
          UNITS_REQUIRED AS units_required,
          UNITS_COMPLETED AS units_completed
        FROM V_STUDENT_REQUIREMENTS
        WHERE EMPLID = ?
          AND EXISTS (
            SELECT 1 FROM PS_SCRTY_STUDENT sec
            WHERE sec.OPRID = ?
              AND sec.EMPLID = V_STUDENT_REQUIREMENTS.EMPLID
          )
        ORDER BY RQRMNT_GROUP
        """,
        (emplid, deps.oprid),
    )
    return [StudentRequirement(**row) for row in rows]


def get_student_financial_aid(deps: DatabaseDeps, emplid: str) -> list[FinancialAidAward]:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          AID_YEAR AS aid_year,
          INSTITUTION AS institution,
          ITEM_TYPE AS item_type,
          AWARD_DESCR AS award,
          AWARD_STATUS AS award_status,
          OFFER_AMOUNT AS offer_amount,
          ACCEPT_AMOUNT AS accept_amount,
          DISBURSEMENT_STATUS AS disbursement_status
        FROM CS_FA_AWARD
        WHERE EMPLID = ?
          AND EXISTS (
            SELECT 1 FROM PS_SCRTY_STUDENT sec
            WHERE sec.OPRID = ?
              AND sec.EMPLID = CS_FA_AWARD.EMPLID
          )
        ORDER BY AID_YEAR, ITEM_TYPE
        """,
        (emplid, deps.oprid),
    )
    return [FinancialAidAward(**row) for row in rows]


def find_students_with_holds(deps: DatabaseDeps) -> list[StudentHold]:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          DISPLAY_NAME AS display_name,
          SRVC_IND_CD AS code,
          SRVC_IND_REASON AS reason,
          START_TERM AS start_term,
          IMPACT AS impact
        FROM V_STUDENT_HOLDS
        WHERE EXISTS (
          SELECT 1 FROM PS_SCRTY_STUDENT sec
          WHERE sec.OPRID = ?
            AND sec.EMPLID = V_STUDENT_HOLDS.EMPLID
        )
        ORDER BY EMPLID, SRVC_IND_CD
        """,
        (deps.oprid,),
    )
    return [StudentHold(**row) for row in rows]


def find_students_with_positive_balance(deps: DatabaseDeps) -> list[StudentBalance]:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          DISPLAY_NAME AS display_name,
          STRM AS term,
          BALANCE AS balance
        FROM V_STUDENT_BALANCE
        WHERE BALANCE > 0
          AND EXISTS (
            SELECT 1 FROM PS_SCRTY_STUDENT sec
            WHERE sec.OPRID = ?
              AND sec.EMPLID = V_STUDENT_BALANCE.EMPLID
          )
        ORDER BY BALANCE DESC
        """,
        (deps.oprid,),
    )
    return [StudentBalance(**row) for row in rows]


def find_students_by_gpa(deps: DatabaseDeps, max_gpa: float) -> list[StudentProfile]:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          DISPLAY_NAME AS display_name,
          FERPA_FLAG AS ferpa_flag,
          ACAD_CAREER AS academic_career,
          ACAD_PROG AS program_code,
          PROG_DESCR AS program,
          ACAD_PLAN AS plan_code,
          PLAN_DESCR AS plan,
          PROG_STATUS AS program_status,
          CUM_GPA AS gpa,
          TOT_CUMULATIVE AS cumulative_units,
          STRM AS term,
          TERM_DESCR AS term_description,
          ENROLL_STATUS AS enrollment_status
        FROM V_STUDENT_360
        WHERE CUM_GPA < ?
          AND EXISTS (
            SELECT 1 FROM PS_SCRTY_STUDENT sec
            WHERE sec.OPRID = ?
              AND sec.EMPLID = V_STUDENT_360.EMPLID
          )
        ORDER BY CUM_GPA, EMPLID
        """,
        (max_gpa, deps.oprid),
    )
    return [StudentProfile(**row) for row in rows]


def find_students_with_incomplete_requirements(deps: DatabaseDeps) -> list[StudentRequirement]:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          DISPLAY_NAME AS display_name,
          ACAD_PLAN AS plan,
          RQRMNT_GROUP AS requirement_group,
          RQRMNT_DESCR AS requirement,
          STATUS AS status,
          UNITS_REQUIRED AS units_required,
          UNITS_COMPLETED AS units_completed
        FROM V_STUDENT_REQUIREMENTS
        WHERE STATUS = 'Not Satisfied'
          AND EXISTS (
            SELECT 1 FROM PS_SCRTY_STUDENT sec
            WHERE sec.OPRID = ?
              AND sec.EMPLID = V_STUDENT_REQUIREMENTS.EMPLID
          )
        ORDER BY EMPLID, RQRMNT_GROUP
        """,
        (deps.oprid,),
    )
    return [StudentRequirement(**row) for row in rows]


def find_students_with_checklist_items(deps: DatabaseDeps) -> list[ChecklistItem]:
    rows = fetch_all(
        deps,
        """
        SELECT
          EMPLID AS emplid,
          DISPLAY_NAME AS display_name,
          CHECKLIST_CD AS checklist,
          CHECKLIST_ITEM_CD AS item,
          ITEM_DESCR AS description,
          STATUS AS status,
          DUE_DT AS due_date,
          ADMIN_FUNCTION AS admin_function
        FROM V_STUDENT_CHECKLISTS
        WHERE EXISTS (
          SELECT 1 FROM PS_SCRTY_STUDENT sec
          WHERE sec.OPRID = ?
            AND sec.EMPLID = V_STUDENT_CHECKLISTS.EMPLID
        )
        ORDER BY EMPLID, DUE_DT, CHECKLIST_CD, CHECKLIST_ITEM_CD
        """,
        (deps.oprid,),
    )
    return [ChecklistItem(**row) for row in rows]


def find_academic_risk_students(deps: DatabaseDeps, max_gpa: float = 3.0) -> list[StudentProfile]:
    return find_students_by_gpa(deps, max_gpa)


def create_student_success_report(deps: DatabaseDeps, emplid: str) -> StudentSuccessReport:
    incomplete = [
        requirement
        for requirement in get_student_requirements(deps, emplid)
        if requirement.status == "Not Satisfied"
    ]
    return StudentSuccessReport(
        profile=get_student_profile(deps, emplid),
        classes=get_student_classes(deps, emplid),
        balance=get_student_balance(deps, emplid),
        holds=get_student_holds(deps, emplid),
        checklists=get_student_checklists(deps, emplid),
        incomplete_requirements=incomplete,
        financial_aid=get_student_financial_aid(deps, emplid),
    )


def money(value: float | int | None) -> str:
    if value is None:
        return "not listed"
    sign = "-" if value < 0 else ""
    amount = abs(float(value))
    if amount.is_integer():
        return f"{sign}${int(amount):,}"
    return f"{sign}${amount:,.2f}"
