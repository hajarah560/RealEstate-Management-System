from django.test import TestCase
from django.urls import reverse
from management.models import Client, Employee, Land, Building, Lease, Payment


class RecordViewsTests(TestCase):
    def setUp(self):
        person = {'firstname': 'Jane', 'lastname': 'Doe', 'contact': '1234567890', 'gender': 'M', 'address': 'Kampala', 'email': 'jane@example.com'}
        self.client_record = Client.objects.create(**person)
        self.employee = Employee.objects.create(**person)
        self.land = Land.objects.create(name='Plot', location='Kampala', status='NT', land_size='10', land_type='Residential')
        self.building = Building.objects.create(name='House', location='Kampala', status='NT')
        self.records = {
            'client': (Client, person, 'firstname', 'Updated'),
            'employee': (Employee, person, 'firstname', 'Updated'),
            'land': (Land, {'name': 'Plot', 'location': 'Kampala', 'status': 'NT', 'land_size': '10', 'land_type': 'Residential'}, 'name', 'Updated'),
            'building': (Building, {'name': 'House', 'location': 'Kampala', 'status': 'NT'}, 'name', 'Updated'),
            'lease': (Lease, {'client': self.client_record.pk, 'employee': self.employee.pk}, 'employee', self.employee.pk),
            'payment': (Payment, {'client': self.client_record.pk, 'employee': self.employee.pk, 'land': self.land.pk, 'building': self.building.pk, 'amount_paid': '100', 'mode_of_payment': 'C'}, 'amount_paid', '200'),
        }

    def test_add_edit_and_delete_records(self):
        for kind, (model, data, field, value) in self.records.items():
            with self.subTest(kind=kind):
                page = reverse(f'{kind}_page')
                response = self.client.get(page)
                self.assertEqual(response.status_code, 200)
                for name in data:
                    self.assertContains(response, f'name="{name}"')
                self.assertRedirects(self.client.post(page, data), page)
                record = model.objects.latest('id')
                edit = reverse(f'edit_{kind}_page', args=[record.pk])
                delete = reverse(f'delete_{kind}_page', args=[record.pk])
                self.assertContains(self.client.get(page), edit)
                self.assertEqual(self.client.get(edit).status_code, 200)
                updated = dict(data, **{field: value})
                self.assertRedirects(self.client.post(edit, updated), page)
                record.refresh_from_db()
                self.assertEqual(getattr(record, field + '_id' if field == 'employee' else field), value)
                self.assertEqual(self.client.get(delete).status_code, 200)
                self.assertTrue(model.objects.filter(pk=record.pk).exists())
                self.assertRedirects(self.client.post(delete), page)
                self.assertFalse(model.objects.filter(pk=record.pk).exists())

    def test_invalid_payment_keeps_form_errors(self):
        response = self.client.post(reverse('payment_page'), {})
        self.assertContains(response, 'This field is required')
        self.assertFalse(Payment.objects.exists())
