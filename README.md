# Estate Desk: Real Estate Management System

A simple Django class project: staff manage clients, employees, land, buildings, leases and payments.

## Run it

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/login/ and sign in with the demo account that ships in `db.sqlite3`:

| Username | Password |
|---|---|
| `admin` | `admin12345` |

Or open http://127.0.0.1:8000/sign_up/ to create your own user.

`db.sqlite3` is tracked in git on purpose, so everyone starts with the same demo data. Committing it also commits any accounts and records you created, so check before you push.

## Demo data

The database already holds 12 employees, 98 clients, 14 land plots, 14 buildings, 20 leases and 57 payments. The names are first and last names taken from a class list and shuffled so no pair matches a real person. The class list itself is not in the repo.

To rebuild the demo data from your own names file:

```
python manage.py seed_demo names.json --reset
```

`names.json` is a list of `{"first_name": ..., "last_name": ...}`. The first 12 become employees and the rest become clients. Land, buildings, leases and payments are generated. `--reset` deletes existing records first (user accounts are kept).

## Status

### Done

- Six apps, each with a model, list page and add / edit / delete through modals: clients, employees, properties (land and buildings), leases, payments.
- Relations: a lease links a client, an employee and either a land plot or a building; a payment links a lease and an employee. `Lease.clean()` validates the lease.
- Dashboard with totals and the recent leases and payments.
- Shared `templates/base.html` with a floating sidebar, plus partials for the sidebar, form fields and table actions.
- Login, logout and sign-up using Django auth. The view functions are protected with `@login_required`.
- Restyled UI: brown and cream palette, three typefaces, flat stat card icons.
- `seed_demo` command for demo data.

### Not done yet

The plan is in `docs/signup-and-marking-plan.md`. It is a plan only and nothing in it is built.

- **Sign-up:** it is still reachable when logged in, it does not log the new user in, and it collects no name or email. Login is also reachable when logged in.
- **Admin site:** every model is registered with the bare default `admin.site.register`, with no customisation.
- **Tests:** there are none.
- `real-estate-frontend/` is the original static HTML mock. The running app does not use it.

## Apps

| App | Holds |
|---|---|
| `dashboard` | Home page totals (no models) |
| `clients` | Client |
| `employees` | Employee |
| `properties` | Land, Building |
| `leases` | Lease (client + land or building) |
| `payments` | Payment (against a lease) |
| `core` | Sign-up view, money filter, `seed_demo` command |

## URLs

| Path | Page |
|---|---|
| `/` | Dashboard |
| `/clients/`, `/employees/`, `/land/`, `/buildings/`, `/leases/`, `/payments/` | List pages. Each has `add/`, `<id>/edit/` and `<id>/delete/` |
| `/login/`, `/logout/`, `/sign_up/` | Auth |
| `/admin/` | Django admin |

The full design plan is in `docs/redesign-plan.md`.
