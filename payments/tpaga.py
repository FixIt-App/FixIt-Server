import json
import requests
import os
import sys


from customer.models import TPagaCustomer, Customer

def create_customer(email, first_name, last_name, customer_id, phone):
    """
        Method that creates a customer in the TPago Database.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic %s" % (os.environ.get('TPAGA_KEY')) 
    }
    body = {
        "email": email,
        "firstName": first_name,
        "gender": "N/A",
        "lastName": last_name,
#        "legalIdNumber": "string",
        "merchantCustomerId": customer_id,
        "phone": phone
    }
    r = requests.post(os.environ.get('TPAGA_HOST') + '/api/customer', data = json.dumps(body), headers = headers)
    if r.status_code >= 200 and r.status_code <= 300:
        response = json.loads(r.text)
        sys.stdout.buffer.write(r.text.encode('utf8'))
        customer = Customer.objects.get(pk = customer_id)
        tpagaCustomer = TPagaCustomer(
            customer = customer,
            tpaga_id = response['id']
        )
        tpagaCustomer.save()
        print('Request successful')
        return True
    else:
        print('Error saving the customer in TPaga')
        print(r.status_code)
        print(r.text)
        return False
