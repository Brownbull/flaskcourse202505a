<!-- 
# Copilot Instructions for This Codebase

## Project Overview
This workspace is a multi-app Flask monorepo with Tailwind CSS for UI, WTForms for forms, SQLAlchemy ORM, and SQLite for persistence. The main active app is `jennyapp`, which demonstrates modern Flask patterns. Other subprojects (dashboard, registration, migration, store, engage) are for reference or legacy.

## Architecture & Data Flow
- **Blueprints:** Each major feature is a Flask blueprint (see `jennyapp/routes.py`).
- **Forms:** WTForms classes in `jennyapp/forms.py` are always kept in sync with SQLAlchemy models in `jennyapp/models.py`.
- **Models:** Relationships are explicit; e.g., `Session` links to `User` and `Patient` via foreign keys.
- **Templates:** Jinja2 templates are organized by feature in `jennyapp/templates/dashboard/`. Tailwind CSS is used for styling, with custom JS in `jennyapp/static/js/` for interactivity.
- **Migrations:** Alembic is used for DB migrations (see `migrations/`).
- **Static Assets:** CSS/JS are in `static/` folders, with Tailwind configured via `tailwind.config.js`.
- **React Frontend:** `bank_fe` is a separate React app, not integrated with Flask.

## Developer Workflows
- **Run Flask App:**
  - Set `FLASK_APP=jennyapp` (or another app)
  - Use `flask run` (recommended) or run `app.py` directly for basic apps
- **DB Migrations:**
  - Use Alembic: `alembic upgrade head`, `alembic revision --autogenerate` in the relevant `migrations/` folder
- **React Frontend:**
  - For `bank_fe`, use `npm start`, `npm run build` (see its README)
- **Testing:**
  - No global test runner; tests (if any) are local to each app
- **Debugging:**
  - Use print statements or Flask's built-in debugger

## Project-Specific Conventions
- **Form/Model Sync:** Always update both WTForms and SQLAlchemy models when adding fields
- **Session Management:** Sessions use Flask-Login; see `routes.py` for login/logout
- **Interactive Tables:** Sorting/filtering is handled via query parameters and Jinja logic (see `sessions` route and template)
- **Delete Buttons:** Only show delete actions when editing an existing record (check for `session_id`)
- **Currency Input:** Amount fields use a `$` prefix and currency label (see `ses_edit.html`)

## Integration Points & Patterns
- **User/Patient Linking:** Sessions reference users and patients by foreign key; ensure these exist before creating a session
- **Custom JS:** All interactivity (dropdowns, menus, dashboard sorting/filtering) is in `jennyapp/static/js/`
- **React/Flask Separation:** No automatic integration; treat `bank_fe` as a standalone frontend

## Examples & Recipes
- **Add a patient field:**
  - Update `PatientForm` in `forms.py`, `Patient` model in `models.py`, and relevant templates in `templates/dashboard/patients/`
- **Add a session:**
  - Use the interactive form in `ses_edit.html`, handle in `routes.py`
- **Sort/filter sessions:**
  - Use query parameters (`?sort=asc&doctor=...&patient=...`) in the sessions route/template

## Key Files/Directories
- `jennyapp/routes.py` — main Flask routes and logic
- `jennyapp/forms.py` — WTForms definitions
- `jennyapp/models.py` — SQLAlchemy models
- `jennyapp/templates/dashboard/` — Jinja2 templates
- `jennyapp/static/js/` — custom JS for UI interactivity
- `migrations/` — Alembic migration scripts
- `bank_fe/` — React frontend for bank app

---
If any conventions or workflows are unclear, provide feedback so this guide can be improved for future AI agents. -->
