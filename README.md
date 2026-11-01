# Campus Lost & Found Management System (CLFM)
## B.Tech CSE 3rd Year - Agile Software Development (Phase 2 Evaluation Submission)
**Bennett University, School of Computer Science Engineering and Technology (SCSET)**

- **Student Name**: Dhruv Saini
- **Enrolment / Roll No.**: S24CSEU0818
- **Course**: Agile Software Development (CSET-455)
- **Section / Batch**: B.Tech CSE, 3rd Year, Batch EB58
- **Faculty / Evaluator**: Dr. Sachin Kumar
- **Project Title**: Campus Lost & Found Management System
- **JIRA Project Name & Key**: Campus Lost and Found System (`CLFM`)
- **JIRA Instance URL**: https://dhruv213112.atlassian.net
- **Evaluation Weightage**: 10 Marks
- **Submission Date**: 01 November 2026

---

## 1. JIRA Project Evidence & Direct Links
- **Project Board URL**: https://dhruv213112.atlassian.net/jira/software/c/projects/CLFM/boards/109
- **Scrum Board**: `CLFM board` (Board ID: 109)
- **Kanban Board**: `CLFM Kanban Board` (Board ID: 111)
- **Project Health Dashboard**: https://dhruv213112.atlassian.net/jira/dashboards/10001
- **Saved JQL Filters**:
  1. `CLFM - Open Lost Reports`: `project = CLFM AND summary ~ "Lost" AND status != Done ORDER BY created DESC` (Filter ID: 10118)
  2. `CLFM - High Priority Items`: `project = CLFM AND priority in (High, Highest) ORDER BY priority DESC` (Filter ID: 10119)
  3. `CLFM - Completed Sprint Stories`: `project = CLFM AND issuetype = Story AND status = Done ORDER BY resolved DESC` (Filter ID: 10120)
  4. `CLFM - Active Sprint 4 Issues`: `project = CLFM AND sprint = 149 ORDER BY Rank ASC` (Filter ID: 10121)

### Sprints Summary (All Completed Prior to 01 Nov 2026)
| Sprint | Name | Dates | Committed Pts | Completed Pts | Goal Met |
|---|---|---|---|---|---|
| Sprint 1 | Sprint 1 | 07 Sep 2026 – 18 Sep 2026 | 6 | 6 | Yes (100%) |
| Sprint 2 | Sprint 2 | 21 Sep 2026 – 02 Oct 2026 | 20 | 20 | Yes (100%) |
| Sprint 3 | Sprint 3 | 05 Oct 2026 – 16 Oct 2026 | 13 | 13 | Yes (100%) |
| Sprint 4 | Sprint 4 | 19 Oct 2026 – 30 Oct 2026 | 10 | 10 | Yes (100%) |
| **Total** | **4 Sprints** | **07 Sep – 30 Oct 2026** | **49** | **49** | **100% (Avg Velocity: 12.25 pts)** |

### Agile Labs (L1–L8) Governance Issues
- **CLFM-21**: L1 - Compare Scrum vs Kanban Boards (Scrum Board 109 vs Kanban Board 111)
- **CLFM-22**: L2 - Sprint Tracking with Burndown and Velocity Charts (Sprint Reports & Burndown analysis)
- **CLFM-23**: L3 - Kanban Flow Analytics (CFD & Control Chart cycle times)
- **CLFM-24**: L4 - JIRA Automation Rules Setup & Verification (Documented & audited)
- **CLFM-25**: L5 - Advanced JQL Queries, Saved Filters & Subscription (4 Saved CLFM filters)
- **CLFM-26**: L6 - Custom Project Health Dashboard (Dashboard 10001 provisioned)
- **CLFM-27**: L7 - Custom Workflow with Statuses & Board Column Mapping (Lifecycle documented)
- **CLFM-28**: L8 - Advanced Workflow Rules (Conditions, Validators & Post-Functions)

---

## 2. Working Application Deliverables (Flask + SQLite)
The application implements end-to-end deliverables across all 4 sprints:
- **Sprint 1**: Student Registration, Password Hashing with Werkzeug, Login, Protected Sessions, Logout.
- **Sprint 2**: Lost and Found Item Reporting Forms, Multi-format Image Uploads (`static/uploads/`), User Report Management (Edit/Delete).
- **Sprint 3**: Real-time Multi-field Keyword Search, Category/Status/Type Filtering, Smart Match Suggestion Engine.
- **Sprint 4**: Ownership Claim Submission, Dual Claims Review Dashboard (Received vs Submitted), Claim Verification (Approve / Reject), and Physical Return Status Handoff.

### How to Run Locally:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```
Open your browser and navigate to:
`http://127.0.0.1:5001` (or `http://127.0.0.1:5000`)

- **Default Test Account**: `dhruv@bennett.edu.in` / `password123`
- Or register a new student account at `/register`.
