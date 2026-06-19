# Database Repository Platform

A web-based project created for the web apps class.


## Key Features
* **Dataset Management:** Users can add, edit, and delete their own datasets, providing metadata such as topic, size class, and complexity.
* **Full-text Search:** Search functionality covering dataset names, authors, descriptions, and community-driven Q&A.
* **Collaborative Q&A:** Registered users can ask questions about datasets; dataset owners can provide answers.
* **Schema Documentation:** Owners can upload database diagrams and DDL scripts to provide technical documentation for their datasets.
* **Data Privacy & Security:**
    * Role-based access control (RBAC) ensures only owners can modify or delete their datasets.
    * Database-level concurrency control (pessimistic locking) to handle simultaneous access.
    * Secure password management and registration workflows.

## Technical Stack
* **Framework:** Django (MVT architecture)
* **Frontend:** Bootstrap 5 with custom SCSS styling
* **Database:** SQLite
* **Search:** Django ORM with Q-objects for query filtering


## Requirements Compliance
This project was developed as a laboratory assignment, meeting requirements for MVC architecture, ORM-based data handling, concurrency management, and full-text indexing.