from square.client import Client
import json

# square API
# run script to delete customer list
client = Client(
    access_token='EAAAEPFPFdbS4HtT08WwOGtHJg0Nit3jU6C_7zrVMY1DRh3NPH_up3cqpGEpozOx',
    environment='production',)

c = client.customers

def list_c():
    r = c.list_customers()
    if r.is_success():
        return r.body
    elif r.is_error():
        return r.errors


def rm_c(id):
    r = c.delete_customer(id)
    if r.is_success():
        return r.body
    elif r.is_error():
        return r.errors


def delete_all_customers():
    x = list_c()["customers"]
    for item in x:
        rm_c(item["id"])
    return "database cleared"

print(delete_all_customers())