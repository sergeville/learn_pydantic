-- PeopleSoft-inspired mock row security for the StudentDB Assistant course.
-- This is not real PeopleSoft security. It models the core teaching concept:
-- an operator ID (OPRID) can only see rows for assigned students.

DROP VIEW IF EXISTS V_ROW_SECURITY_ACCESS;
DROP TABLE IF EXISTS PS_SCRTY_STUDENT;
DROP TABLE IF EXISTS PS_SCRTY_OPR;

CREATE TABLE PS_SCRTY_OPR (
  OPRID TEXT PRIMARY KEY,
  DESCR TEXT NOT NULL,
  ACCESS_PROFILE TEXT NOT NULL
);

CREATE TABLE PS_SCRTY_STUDENT (
  OPRID TEXT NOT NULL,
  EMPLID TEXT NOT NULL,
  ACCESS_REASON TEXT NOT NULL,
  PRIMARY KEY (OPRID, EMPLID),
  FOREIGN KEY (OPRID) REFERENCES PS_SCRTY_OPR(OPRID)
);

INSERT INTO PS_SCRTY_OPR (OPRID, DESCR, ACCESS_PROFILE) VALUES
  ('REGISTRAR_ALL', 'Registrar super user for training', 'All students'),
  ('ADVISOR_COMP', 'Computer Science advisor for training', 'Computer Science students'),
  ('ADVISOR_BUSA', 'Business Analytics advisor for training', 'Business Analytics students'),
  ('ADVISOR_LIMITED', 'Limited advisor for training', 'Two assigned students'),
  ('NO_ACCESS', 'Operator with no student row access', 'No students');

INSERT INTO PS_SCRTY_STUDENT (OPRID, EMPLID, ACCESS_REASON)
SELECT 'REGISTRAR_ALL', EMPLID, 'Registrar training access'
FROM CS_CC_PERSON;

INSERT INTO PS_SCRTY_STUDENT (OPRID, EMPLID, ACCESS_REASON)
SELECT 'ADVISOR_COMP', EMPLID, 'Program advisor access: COMP'
FROM V_STUDENT_360
WHERE ACAD_PROG = 'COMP';

INSERT INTO PS_SCRTY_STUDENT (OPRID, EMPLID, ACCESS_REASON)
SELECT 'ADVISOR_BUSA', EMPLID, 'Program advisor access: BUSA'
FROM V_STUDENT_360
WHERE ACAD_PROG = 'BUSA';

INSERT INTO PS_SCRTY_STUDENT (OPRID, EMPLID, ACCESS_REASON) VALUES
  ('ADVISOR_LIMITED', '0001005', 'Assigned advisee'),
  ('ADVISOR_LIMITED', '0001006', 'Assigned advisee');

CREATE VIEW V_ROW_SECURITY_ACCESS AS
SELECT
  opr.OPRID,
  opr.DESCR,
  opr.ACCESS_PROFILE,
  sec.EMPLID,
  p.DISPLAY_NAME,
  p.FERPA_FLAG,
  sec.ACCESS_REASON
FROM PS_SCRTY_OPR opr
LEFT JOIN PS_SCRTY_STUDENT sec
  ON opr.OPRID = sec.OPRID
LEFT JOIN CS_CC_PERSON p
  ON sec.EMPLID = p.EMPLID;
