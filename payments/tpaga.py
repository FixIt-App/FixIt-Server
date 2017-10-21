import json
import requests
import os
import sys

from datetime import datetime

from customer.models import TPagaCustomer, Customer, CreditCard
from work.models import Transaction, TransactionItem, Work


def charge_credit_card(transaction_id):
    """
        Method that charges to a credit card
        {
            "amount": 10000,
            "creditCard": "8jpasvh9evs0al91csti9jkqll85bok0",
            "currency": "COP",
            "description": "Pago de servicios",
            "iacAmount": 0,
            "installments": 1,
            "orderId": "1234",
            "taxAmount": 2000,
            "thirdPartyId": "1",
            "tipAmount": 0
        }
    """
    try: 
        transaction = Transaction.objects.get(pk = transaction_id)
        sub_total = TransactionItem.objects.get(trx__id = transaction.id, item_type = 'SUBTOTAL')
        taxes = TransactionItem.objects.get(trx__id = transaction.id, item_type = 'IVA')
        work = Work.objects.get(pk = transaction.work.id)
        tpaga_customer = TPagaCustomer.objects.get(customer__id = work.customer.id)
        credit_card = CreditCard.objects.get(tpagaCustomer__id = tpaga_customer.id)
        content = {
            "amount": sub_total.price,
            "creditCard": credit_card.credit_card_id,
            "currency": "COP",
            "description": work.description,
            "iacAmount": 0,
            "installments": 24,
            "orderId": transaction.receipt_number,
            "taxAmount": taxes.price,
            "thirdPartyId": "1",
            "tipAmount": 0
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Basic %s" % (os.environ.get('TPAGA_KEY')) 
        }
        uri = os.environ.get('TPAGA_HOST')  + '/api/charge/credit_card'
        r = requests.post(uri, data = json.dumps(content), headers = headers)
        if r.status_code >= 200 and r.status_code <= 300:
            print('Transaction %s finshed succesfully' % str(transaction.id))
            response = json.loads(r.text)
            transaction.timestamp = datetime.now()
            transaction.third_party_response = r.text
            transaction.credit_card = credit_card
            transaction.state = 'PAYED'
            transaction.save()
        else:
            raise Exception("Error fatal al procesar el pago D:")
    except Transaction.DoesNotExist:
        raise Exception("Transaction not found")
    except TransactionItem.DoesNotExist:
        raise Exception("TransactionItem not found")
    except Work.DoesNotExist:
        raise Exception("Work not found")
    except TPagaCustomer.DoesNotExist:
        raise Exception("tpaga customer not found")
    except CreditCard.DoesNotExist:
        raise Exception("Credit card not found")

def get_credit_card_data(customer_id, credit_card_id):
    """
        Method that GETs credit carda data
        Sample response
        {
            "id": "l0nq6d3b43io21o0ajgfjst4i0el5onc",
            "bin": "411111",
            "type": "VISA",
            "expirationMonth": "08",
            "expirationYear": "2020",
            "lastFour": "1111",
            "customer": "dm5ccaath32fpmgb1gs0drsi70mgi85i",
            "cardHolderName": "John Smith",
            "cardHolderLegalIdNumber": null,
            "cardHolderLegalIdType": null,
            "addressLine1": null,
            "addressLine2": null,
            "addressCity": null,
            "addressState": null,
            "addressPostalCode": null,
            "addressCountry": null,
            "fingerprint": "7bf64302fe8a3726158c8694fc22446b10560b1938a78ee9baef5ef0eb7bcab7"
    }
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Basic %s" % (os.environ.get('TPAGA_KEY')) 
    }
    uri = os.environ.get('TPAGA_HOST')  + '/api/customer/%s/credit_card/%s' % (customer_id, credit_card_id)
    print('making request to uri %s' % uri)
    r = requests.get(uri, headers = headers)
    if r.status_code >= 200 and r.status_code <= 300:
        print('getting card from tpaga database')
        response = json.loads(r.text)
        return response
    else:
        print('Error getting card from tpago db')
        print(r.status_code)
        return False

def associate_credit_card(credit_card_token, tpagaCust):
    """
        Method that associates a credit card to a customer
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Basic %s" % (os.environ.get('TPAGA_KEY')) 
    }
    body = {
        "skipLegalIdCheck": False,
        "token": credit_card_token
    }
    uri = os.environ.get('TPAGA_HOST') + '/api/customer/%s/credit_card_token' % tpagaCust.tpaga_id
    print('Making a request tu uri %s' % uri)
    r = requests.post(uri, data = json.dumps(body), headers = headers)
    if r.status_code >= 200 and r.status_code < 300:
        print('Saved customer data in TPAGO database')
        response = json.loads(r.text)
        print(response)
        credit_card = CreditCard(
            credit_card_id = response['id'], 
            card_holder_name = response['cardHolderName'], 
            last_four = response['lastFour'], 
            type = response['type'], 
            tpagaCustomer = tpagaCust)
        credit_card.save()
        return credit_card
    else:
        print('Error saving the customer in TPaga')
        print(r.status_code)
        return False


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
    if r.status_code >= 200 and r.status_code < 300:
        response = json.loads(r.text)
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
        return False
