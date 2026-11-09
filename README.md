# Estate Desk: Real Estate Management System

A simple Django class project: staff manage clients, employees, land, buildings, leases and payments.

## Run it

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/sign_up/ to create a user, then log in.

## Apps

| App | Holds |
|---|---|
| `dashboard` | Home page totals (no models) |
| `clients` | Client |
| `employees` | Employee |
| `properties` | Land, Building |
| `leases` | Lease (client + land or building) |
| `payments` | Payment (against a lease) |
| `core` | Sign-up view, search helper, money filter |

The full plan is in `docs/redesign-plan.md`.
