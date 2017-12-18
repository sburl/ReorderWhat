#this file creates purchase orders given what to order (emails and csvs)

import pandas as pd

#make email text from template
def makeEmail(contact, email):

    template = """Hi %s,
Please send any available items in the attached spreadsheet. It is also ok to backorder any items on the spreadsheet that are not available, but don't add to existing backorders.
Thanks!
Bret

%s""" % (contact, email)

    return template

#make csv and email text for each vendor
def makeSeperate(vendors, orderbyVendor, modelType, exportPath, runCount):
    for vendor in orderbyVendor:

        if runCount == 0:
            nameAdd = ""
        else:
            nameAdd = " " + str(runCount)

        csvfile = exportPath + "/" + vendor + nameAdd + ".csv"

        data = orderbyVendor[vendor]
        df = pd.DataFrame(data)
        df.columns = ["sku", "name", "qty"]
        df.to_csv(csvfile, encoding='utf-8', index = False)

        if isinstance(vendors[vendor][1], str):
            contact = vendors[vendor][1]
        else:
            contact = "--"

        if isinstance(vendors[vendor][2], str):
            email = vendors[vendor][2]
        else:
            email = "--"

        file = open(exportPath + "/" + vendor + " " + "Email" + nameAdd,"w+")
        template = makeEmail(contact, email)
        file.write(template)
        file.close()

#convert toOrder list to a dataframe
def createCSV(toOrder, vendors, modelType, exportPath, runCount):

    df = pd.DataFrame(toOrder)

    df.columns = ["sku", "vendor", "name", "qty"]

    #make a csv for each vendor
    orderbyVendor = dict()
    for index in range(len(df["vendor"])):
        vendor = df["vendor"][index]
        sku = df["sku"][index]
        name = df["name"][index]
        qty = df["qty"][index]
        if vendor in orderbyVendor:
            orderbyVendor[vendor] += [(sku, name, qty)]
        else:
            orderbyVendor[vendor] = [(sku, name, qty)]

    makeSeperate(vendors, orderbyVendor, modelType, exportPath, runCount)
