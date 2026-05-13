-- Student self-service row security for the StudentDB Assistant course.
-- Each STUDENT_<EMPLID> operator can see only their own student row.

INSERT OR IGNORE INTO PS_SCRTY_OPR (OPRID, DESCR, ACCESS_PROFILE)
SELECT
  'STUDENT_' || EMPLID AS OPRID,
  DISPLAY_NAME || ' self-service login' AS DESCR,
  'Student self-service: own row only' AS ACCESS_PROFILE
FROM CS_CC_PERSON;

INSERT OR IGNORE INTO PS_SCRTY_STUDENT (OPRID, EMPLID, ACCESS_REASON)
SELECT
  'STUDENT_' || EMPLID AS OPRID,
  EMPLID,
  'Student self-service access to own row' AS ACCESS_REASON
FROM CS_CC_PERSON;
