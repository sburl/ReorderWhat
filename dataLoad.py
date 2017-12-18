#this file loads data from the specified CSVs and passes it on

import pandas as pd
import datetime, copy

#from 15-112 website
def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

#makes dict of vendors and their info
def getVendors(path):

    consignStatusTag = "Consignment"
    nameTag = "Name"
    cNameTag = "Contact Name"
    cEmailTag = "Contact Email"

    df = pd.read_csv(path)

    vendors = dict()

    for index in range(len(df[consignStatusTag])):
        name = df[nameTag][index]
        consignStatus = df[consignStatusTag][index]
        contactName = df[cNameTag][index]
        contactEmail = df[cEmailTag][index]
        vendors[name] = (consignStatus, contactName, contactEmail)

    return vendors

#test from terminal - unicode error otherwise
def getSales(path):

    dateTag = "Date"
    skuTag = "SKU"
    salesPriceTag = "Sales Price"
    nameTag = "Name"
    qtyTag = "Qty"

    df = pd.read_csv(path)

    sales = dict()

    #convert date into days after first date in list
    df[dateTag] = pd.to_datetime(df[dateTag])
    df["dateNum"] = df[dateTag].dt.strftime('%y%j')
    df["dateNum"] = (df["dateNum"]).astype(int)

    #map name to sales date/quantity/cost
    for index in range(len(df[nameTag])):
        sku = df[skuTag][index]
        if sku in sales:
            sales[sku] += [(df[qtyTag][index],
            df["dateNum"][index], df[salesPriceTag][index])]
        else:
            sales[sku] = [(df[qtyTag][index],
            df["dateNum"][index], df[salesPriceTag][index])]

    return sales

#pull cost/salePrice data from .csv and put in dict
def getPnC(path):

    nameTag = "Name"
    inPriceTag = "Price"
    costTag = "Cost"
    skuTag = "SKU"
    qtyTag = "Qty"
    inVendorTag = "Vendor"

    dataPnC = dict()

    #read from csv + find profit/ margin
    df = pd.read_csv(path)

    df[costTag] = df[costTag].astype(float)
    df[inPriceTag] = df[inPriceTag].astype(float)

    df["profit"] = df[inPriceTag] - df[costTag]
    df["margin"] = df["profit"] / df[inPriceTag]

    ## ammend to index dataPnC by SKU
    #map sku to cost data
    for index in range(len(df[skuTag])):
        sku = df[skuTag][index]
        dataPnC[sku] = (df[inPriceTag][index], df[costTag][index],
        df["profit"][index], df["margin"][index], df[qtyTag][index],
        df[nameTag][index], df[skuTag][index], df[inVendorTag][index])

    return dataPnC

#remove consiged items from dataPnC
def cleanPnC(dataPnC, vendors):

    consignID = "Consignment"

    cleanDataPnC = copy.deepcopy(dataPnC)

    for item in dataPnC:
        vendorID = cleanDataPnC[item][7]
        if vendors[vendorID][0] == consignID:
            del cleanDataPnC[item]

    return cleanDataPnC

#find item with highest profit margin
def findHighest(dataPnC):
    #find highest margin product in dict
    hM = 0
    hMKey = None
    for key in dataPnC:
        newM = dataPnC[key][3]
        if newM > hM and almostEqual(newM, 1.0) != True:
            hMKey = key
            hM = dataPnC[key][3]

    return dataPnC[hMKey]

#this file buckets an item's sales history by a time period

#buckets sales for given item by month (only for this year)
def getYTDMonthly(history):

    #find end of dataset - today's date for this model
    today = datetime.datetime.now().date()
    todayJulian = today.strftime('%y%j')
    maxMonth = datetime.datetime.strptime(todayJulian, '%y%j').month
    currentYear = datetime.datetime.strptime(todayJulian, '%y%j').year

    #map sales to month
    keys = list(range(1,maxMonth + 1))
    monthly = dict.fromkeys(keys, 0)
    for index in range(len(history)):
        day = str(history[index][1])
        month = datetime.datetime.strptime(day, '%y%j').month
        year = datetime.datetime.strptime(day, '%y%j').year
        if year == currentYear:
            monthly[month] += 1

    return monthly

#buckets sales for given item by month (for all years)
def getAllMonthly(history):

    #find end of dataset - today's date for this model
    today = datetime.datetime.now().date()
    todayJulian = today.strftime('%y%j')
    maxMonth = datetime.datetime.strptime(todayJulian, '%y%j').month
    maxYear = datetime.datetime.strptime(todayJulian, '%y%j').year
    minYear = history[0][0]

    #map sales to month
    keys = list(range(1,maxHalf + 1 + (maxYear - minYear)))
    monthly = dict.fromkeys(keys, 0)
    for index in range(len(history)):
        day = str(history[index][1])
        month = datetime.datetime.strptime(day, '%y%j').month
        year = datetime.datetime.strptime(day, '%y%j').year
        yearAdd = (year - minYear) * 12
        monthly[month + yearAdd] += 1

    return monthly

#buckets sales for given item by quarter (only for this year)
def getYTDQuarter(history):

    #find end of dataset - today's date for this model
    today = datetime.datetime.now().date()
    todayJulian = today.strftime('%y%j')
    maxMonth = datetime.datetime.strptime(todayJulian, '%y%j').month
    maxQuarter = ((maxMonth - 1) // 3) + 1
    currentYear = datetime.datetime.strptime(todayJulian, '%y%j').year

    #map sales to quarter
    keys = list(range(1,maxQuarter + 1))
    quarterly = dict.fromkeys(keys, 0)
    for index in range(len(history)):
        day = str(history[index][1])
        month = datetime.datetime.strptime(day, '%y%j').month
        quarter = ((month - 1) // 3) + 1
        year = datetime.datetime.strptime(day, '%y%j').year
        if year == currentYear:
            quarterly[quarter] += 1

    return quarterly

#buckets sales for given item by quarter (for all years)
def getAllQuarter(history):

    #find end of dataset - today's date for this model
    today = datetime.datetime.now().date()
    todayJulian = today.strftime('%y%j')
    maxMonth = datetime.datetime.strptime(todayJulian, '%y%j').month
    maxQuarter = ((maxMonth - 1) // 3) + 1
    maxYear = datetime.datetime.strptime(todayJulian, '%y%j').year
    minYear = history[0][0]

    #map sales to quarter
    keys = list(range(1,maxHalf + 1 + (maxYear - minYear)))
    quarterly = dict.fromkeys(keys, 0)
    for index in range(len(history)):
        day = str(history[index][1])
        month = datetime.datetime.strptime(day, '%y%j').month
        year = datetime.datetime.strptime(day, '%y%j').year
        yearAdd = (year - minYear) * 4
        quarter = ((month - 1) // 3) + 1
        quarterly[quarter + yearAdd] += 1

    return quarterly

#buckets sales for given item by 1/2 year (only for this year)
#this requires you to be in the second half of the year
def getYTDHalf(history):

    #find end of dataset - today's date for this model
    today = datetime.datetime.now().date()
    todayJulian = today.strftime('%y%j')
    maxMonth = datetime.datetime.strptime(todayJulian, '%y%j').month
    maxHalf = ((maxMonth - 1) // 6) + 1
    currentYear = datetime.datetime.strptime(todayJulian, '%y%j').year

    #map sales to quarter
    keys = list(range(1,maxHalf + 1))
    halfSplit = dict.fromkeys(keys, 0)
    for index in range(len(history)):
        day = str(history[index][1])
        month = datetime.datetime.strptime(day, '%y%j').month
        half = ((month - 1) // 6) + 1
        year = datetime.datetime.strptime(day, '%y%j').year
        if year == currentYear:
            halfSplit[half] += 1

    return halfSplit

#buckets sales for given item by 1/2 year (for all years)
#this requires more than 1 year of data to properly run
def getAllHalf(history):

    #find end of dataset - today's date for this model
    today = datetime.datetime.now().date()
    todayJulian = today.strftime('%y%j')
    maxMonth = datetime.datetime.strptime(todayJulian, '%y%j').month
    maxHalf = ((maxMonth - 1) // 6) + 1
    maxYear = datetime.datetime.strptime(todayJulian, '%y%j').year
    minYear = history[0][0]

    #map sales to 6 month period
    keys = list(range(1,maxHalf + 1 + (maxYear - minYear)))
    halfSplit = dict.fromkeys(keys, 0)
    for index in range(len(history)):
        day = str(history[index][1])
        month = datetime.datetime.strptime(day, '%y%j').month
        year = datetime.datetime.strptime(day, '%y%j').year
        yearAdd = (year - minYear) * 2
        half = ((month - 1) // 6) + 1
        halfSplit[half + yearAdd] += 1

    return halfSplit

#finds sales history and runs selected model
def find(sku, sales, model):

    history = sales[sku]

    if model == "YTDMonth":
        dataSet = getYTDMonthly(history)
    elif model == "YTDQuarter":
        dataSet = getYTDQuarter(history)
    elif model == "YTDHalf":
        dataSet = getYTDHalf(history)
    elif model == "AllMonth":
        dataSet = getYTDMonthly(history)
    elif model == "AllQuarter":
        dataSet = getYTDQuarter(history)
    elif model == "AllHalf":
        dataSet = getAllHalf(history)

    return dataSet
