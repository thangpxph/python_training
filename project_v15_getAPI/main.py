import requests
import csv
r = requests.get(
    "https://817b032f2f21572ca1b1ccdc704d2b5b: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@thangpx.myshopify.com/admin/api/2021-01/customers.json")

re = r.json()['customers']

def getList(dict):
    return list(dict.keys())
fieldname = getList(re[0])

with open('customer.csv', mode='w') as csv_file:

    writer = csv.DictWriter(csv_file, fieldnames=getList(re[0]))

    writer.writeheader()
    for i in re:
        writer.writerow(i)
