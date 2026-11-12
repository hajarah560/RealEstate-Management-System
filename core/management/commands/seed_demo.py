"""Fill the database with demo data.

Usage:  python manage.py seed_demo names.json [--reset]

names.json is a list of {"first_name": ..., "last_name": ...}. The first 12 people become
employees and the rest become clients. Land, buildings, leases and payments are made up.
"""

# Plain English: a "management command" is a script you run from the terminal with
# `python manage.py <name>`. Django finds this one because the file sits in
# core/management/commands/, and the file name (seed_demo) becomes the command name.
# Run it like this:
#     python manage.py seed_demo names.json            (only works on an empty database)
#     python manage.py seed_demo names.json --reset    (wipes the records first, then refills)
# Technical: --reset deletes every Payment, Lease, Client, Employee, Land and Building row.
# User accounts are not touched.

# json reads the names file, random makes up the data, re cleans names for email addresses.
import json
import random
import re
# date and timedelta do date arithmetic (a lease starts on a date and ends a year or more later).
from datetime import date, timedelta

# Plain English: the base class every command extends, and the way to stop with a clear error.
# Technical: CommandError prints the message and exits without a scary traceback.
from django.core.management.base import BaseCommand, CommandError
# Plain English: all-or-nothing. Technical: transaction.atomic undoes everything if an error
# happens half way, so we never end up with a half-filled database.
from django.db import transaction
from django.utils import timezone

# The models we create rows for.
from clients.models import Client
from employees.models import Employee
from leases.models import Lease
from payments.models import Payment
from properties.models import Building, Land

# Lists of made-up ingredients; the code below picks from them at random.
PLACES = ["Kampala", "Wakiso", "Entebbe", "Mukono", "Jinja", "Mbarara", "Gulu", "Masaka"]
AREAS = ["Ntinda", "Bugolobi", "Kololo", "Muyenga", "Najjera", "Kira", "Namugongo", "Makindye", "Munyonyo", "Kansanga"]
LAND_TYPES = ["Residential", "Commercial", "Agricultural"]
LAND_SIZES = ["50 x 100 ft", "100 x 100 ft", "0.5 acre", "1 acre", "2 acres", "5 acres"]
BUILDING_NAMES = ["Lakeview Apartments", "Central Plaza", "Hilltop Villas", "Garden Court", "Sunrise Offices",
                  "Riverside Flats", "Acacia House", "Crown Towers", "Palm Gardens", "Summit Place",
                  "Greenfield Lodge", "Market Square Shops", "Bayview Residences", "Unity Arcade"]
# Payment methods to pick from.
MODES = ["Cash", "Cheque", "Bank Transfer"]
EMPLOYEE_COUNT = 12


class Command(BaseCommand):
    help = "Fill the database with demo clients, employees, land, buildings, leases and payments."

    def add_arguments(self, parser):
        parser.add_argument("names_file", help="JSON list of first_name / last_name pairs")
        parser.add_argument("--reset", action="store_true", help="Delete existing records first")

    # Plain English: handle() is what runs when you type the command.
    # Technical: @transaction.atomic wraps the whole function in one database transaction.
    @transaction.atomic
    def handle(self, *args, **options):
        with open(options["names_file"], encoding="utf-8") as f:
            names = json.load(f)
        if len(names) <= EMPLOYEE_COUNT:
            raise CommandError(f"Need more than {EMPLOYEE_COUNT} names.")

        # --reset: clear the old data (children first: payments depend on leases, leases on
        # clients, so deleting in this order avoids foreign key errors). Without --reset we
        # refuse to run on a database that already has data, so nobody overwrites real records by accident.
        if options["reset"]:
            for model in (Payment, Lease, Client, Employee, Land, Building):
                model.objects.all().delete()
        elif Client.objects.exists() or Employee.objects.exists() or Land.objects.exists():
            raise CommandError("The database already has records. Use --reset to replace them.")

        # Plain English: a random generator started from a fixed number (7), so every run
        # produces the same "random" data and everyone in the class sees the same demo.
        # Technical: a seeded random.Random instance instead of the global random module.
        rng = random.Random(7)
        today = timezone.localdate()

        # Builds the shared details of a person. Employees and clients both use it,
        # because they have the same fields. The slug keeps only a-z so emails are valid.
        def person(p):
            slug = lambda s: re.sub(r"[^a-z]", "", s.lower())
            return dict(
                first_name=p["first_name"], last_name=p["last_name"], gender=rng.choice("MF"),
                contact=f"+2567{rng.randint(0, 99999999):08d}",
                email=f"{slug(p['first_name'])}.{slug(p['last_name'])}@example.com",
                address=f"{rng.choice(AREAS)}, {rng.choice(PLACES)}",
            )

        # Step 1: the first 12 names become employees, everyone else becomes a client.
        employees = [Employee.objects.create(**person(p)) for p in names[:EMPLOYEE_COUNT]]
        clients = [Client.objects.create(**person(p)) for p in names[EMPLOYEE_COUNT:]]

        # Step 2: made-up land and buildings, all starting as Available ("A").
        lands = [Land.objects.create(
            name=f"Plot {rng.randint(1, 200)} {rng.choice(AREAS)}", location=rng.choice(PLACES),
            land_size=rng.choice(LAND_SIZES), land_type=rng.choice(LAND_TYPES),
            price=rng.randrange(25, 400, 5) * 1_000_000, status="A") for _ in range(14)]
        buildings = [Building.objects.create(
            name=name, location=f"{rng.choice(AREAS)}, {rng.choice(PLACES)}",
            price=rng.randrange(150, 1500, 10) * 1_000_000, status="A") for name in BUILDING_NAMES]

        # 20 leases, each on a different property. Leased properties are marked Taken.
        free = lands + buildings
        rng.shuffle(free)
        payments = 0
        for prop in free[:20]:
            start = date(2025, 1, 1) + timedelta(days=rng.randint(0, 600))
            lease = Lease.objects.create(
                client=rng.choice(clients), employee=rng.choice(employees),
                land=prop if isinstance(prop, Land) else None,
                building=prop if isinstance(prop, Building) else None,
                start_date=start, end_date=start + timedelta(days=365 * rng.randint(1, 3)))
            prop.status = "T"
            prop.save()
            # one payment every month since the lease started, at most 4 of them
            for month in range(rng.randint(1, 4)):
                paid_on = start + timedelta(days=30 * month + rng.randint(0, 10))
                if paid_on <= today:
                    Payment.objects.create(
                        lease=lease, employee=rng.choice(employees), mode=rng.choice(MODES),
                        amount=rng.randrange(1_000_000, 20_000_000, 50_000), date=paid_on)
                    payments += 1

        # Step 3 (done): print a green summary. Technical: self.stdout is used instead of print()
        # so Django controls the output.
        self.stdout.write(self.style.SUCCESS(
            f"Created {len(employees)} employees, {len(clients)} clients, {len(lands)} land, "
            f"{len(buildings)} buildings, 20 leases and {payments} payments."))
