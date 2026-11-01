# Campus Lost & Found Management System
## B.Tech CSE 3rd Year - Agile Software Development (Phase 2 Submission)
**Bennett University, Greater Noida**

- **Student Name**: Dhruv Saini
- **Enrolment / Roll No.**: S24CSEU0818
- **Project Title**: Campus Lost & Found Management System
- **JIRA Project Name & Key**: Campus Lost & Found Management System (CLF)
- **JIRA Instance URL**: https://dhruv213112.atlassian.net
- **Submission Date**: 01 November 2026

---

## 1. JIRA Project Evidence & Links
- **Project URL**: https://dhruv213112.atlassian.net/jira/software/c/projects/CLF/boards/107
- **Scrum Board**: `CLF board` (Board ID: 107)
- **Kanban Board**: `CLF Kanban Board` (Board ID: 108)
- **Project Dashboard**: https://dhruv213112.atlassian.net/jira/dashboards/10001
- **Saved JQL Filters**:
  1. `CLF - Open Lost Items`: `project = CLF AND summary ~ "Lost" AND status != Done` (Filter ID: 10113)
  2. `CLF - High Priority Items`: `project = CLF AND priority in (High, Highest)` (Filter ID: 10114)
  3. `CLF - Active Sprint Issues`: `project = CLF AND sprint in openSprints()` (Filter ID: 10115)
  4. `CLF - Completed Stories`: `project = CLF AND issuetype = Story AND status = Done` (Filter ID: 10116)
  5. `CLF - Kanban Filter`: `project = CLF ORDER BY Rank ASC` (Filter ID: 10117)

### Sprints Summary
| Sprint | Name | Status | Committed Pts | Completed Pts | Goal Met |
|---|---|---|---|---|---|
| Sprint 1 | CLF Sprint 1 | Closed | 6 | 6 | Yes (100%) |
| Sprint 2 | CLF Sprint 2 | Closed | 20 | 20 | Yes (100%) |
| Sprint 3 | CLF Sprint 3 | Closed | 13 | 13 | Yes (100%) |
| Sprint 4 | CLF Sprint 4 | Active | 10 | 3 (In Progress) | Active |

### Labs L1–L8 Coverage
- **CLF-21**: L1 - Compare Scrum vs Kanban Boards
- **CLF-22**: L2 - Sprint Tracking with Burndown and Velocity Charts
- **CLF-23**: L3 - Kanban Flow Analytics (CFD & Control Chart)
- **CLF-24**: L4 - JIRA Automation Rules Setup & Verification
- **CLF-25**: L5 - Advanced JQL Queries, Saved Filters & Subscription
- **CLF-26**: L6 - Custom Project Health Dashboard
- **CLF-27**: L7 - Custom Workflow with Statuses & Board Column Mapping
- **CLF-28**: L8 - Advanced Workflow Rules (Conditions, Validators & Post-Functions)

---

## 2. Working Application Deliverables (Flask + SQLite)
The application implements deliverables across all 4 sprints:
- **Sprint 1**: Student Registration, Password Hashing, Login, Session Management, Logout.
- **Sprint 2**: Report Lost/Found Items, Photo Upload (`static/uploads/`), CRUD Report Editing.
- **Sprint 3**: Multi-field Keyword Search, Category/Status Filtering, Smart Match Engine.
- **Sprint 4**: Ownership Claim Submission, Verification Review Panel (Verify / Reject / Return).

### How to Run Locally:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Visit: `http://127.0.0.1:5000`
- **Default Login**: `dhruv@bennett.edu.in` / `password123` (or click Register)
