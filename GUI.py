#this file allows user to identify data file, provides help and shows output

from tkinter import filedialog
from tkinter import *
import pandas as pd
import random

# pandasTable used in acordance with guidelines outlined in documentation
# citation requested:
#Farrell, D 2016 DataExplore: An Application for General Data Analysis in Research and Education.
#Journal of Open Research Software, 4: e9, DOI: http://dx.doi.org/10.5334/jors.94
from pandastable import Table, TableModel

from findProfit import *
from dataLoad import *
from purchaseOrder import createCSV

####################################
# framework from 15-112 website
####################################

def init(data):

    #initialize used supplied parameters
    data.inPath = ""
    data.salesPath = ""
    data.vendorPath = ""
    data.exportPath = ""
    data.model = "YTD"
    data.capital = ""
    data.hasConsign = True
    data.results = []
    data.selectedResult = None
    data.runTable = False
    data.df = []

    #display parameters
    data.vSplit = 12
    data.hSplitR = 15
    data.hSplit = data.width // 16
    data.bigfont = "Avenir 50 bold"
    data.muchbigger = "Avenir 30 bold"
    data.biggerfont = "Avenir 20 bold"
    data.font = "Avenir 18 bold"
    data.smallfont = "Avenir 15 bold"
    data.smallerfont = "Avenir 13 bold"
    data.mainColor = "darkBlue"

    #button parameters
    data.buttonUpperY = 515
    data.buttonHeight = 50
    #two buttons on bottom or otherwise
    data.buttonLowerY = data.buttonUpperY + data.buttonHeight
    data.leftButtonLeft = data.width * 2 // 10
    data.buttonWidth = data.width * 2.5 // 10
    data.leftButtonRight = data.leftButtonLeft + data.buttonWidth
    data.rightButtonLeft = data.width * 5.5 // 10
    data.rightButtonRight = data.rightButtonLeft + data.buttonWidth
    data.secondHUpper = data.buttonHeight * 1.5
    data.secondHLower = data.buttonHeight * .5
    data.thirdHUpper = data.buttonHeight * 3
    data.thirdHLower = data.buttonHeight * 2
    #middle button on bottom or otherwise
    data.mButtonWidth = (data.leftButtonRight - data.leftButtonLeft) * 1.5
    data.mButtonMiddle = (data.leftButtonLeft + data.rightButtonRight) // 2
    #3 buttons on bottom
    data.overallWidth = data.leftButtonLeft + data.leftButtonRight
    data.threeButtonWidth = data.overallWidth // 4
    data.leftLeftX = data.leftButtonLeft - 0.5 * data.threeButtonWidth
    data.leftRightX = data.leftButtonLeft + 1 * data.threeButtonWidth
    data.middleLeftX = data.leftButtonLeft + 1.25 * data.threeButtonWidth
    data.middleRightX = data.leftButtonLeft + 2.75 * data.threeButtonWidth
    data.rightLeftX = data.leftButtonLeft + 3 * data.threeButtonWidth
    data.rightRightX = data.leftButtonLeft + 4.5 * data.threeButtonWidth

    #states
    data.basis = True
    data.chooseFiles = False
    data.modelSelect = False
    data.review = False
    data.runAnimation = False
    data.actualRun = False
    data.resulting = False
    data.viewMonth = False
    data.viewQuarterly = False
    data.viewSixMonth = False

    data.typeModel = None
    data.runAlready = False
    data.makeCSV = False
    data.runCSVcount = 0
    data.sales = ""
    data.dataPnC = ""
    data.vendors = ""
    data.photo = ""

# runs appropriate button from click
def mousePressed(event, data):

    ## all back/next buttons

    #left/right button can be clicked everywhere but two states
    if data.basis != True and data.resulting != True:
        if (event.x >= data.leftButtonLeft
        and event.x <= data.leftButtonRight
        and event.y >= data.buttonUpperY
        and event.y <= data.buttonLowerY):
            leftButtonClicked(data)

        elif (event.x >= data.rightButtonLeft
        and event.x <= data.rightButtonRight
        and event.y >= data.buttonUpperY
        and event.y <= data.buttonLowerY):
            rightButtonClicked(data)

    #middle bottom button can only be clicked in basis
    elif data.basis == True:
        if (event.x >= data.mButtonMiddle - (0.5 * data.mButtonWidth)
        and event.x <= data.mButtonMiddle + (0.5 * data.mButtonWidth)
        and event.y >= data.buttonUpperY
        and event.y <= data.buttonLowerY):
            middleBottonClicked(data)

    #bottom 3 can only be clicked in results
    elif data.resulting == True:

        if (event.x >= data.leftLeftX
        and event.x <= data.leftRightX
        and event.y >= data.buttonUpperY
        and event.y <= data.buttonLowerY):
            leftThirdClicked(data)

        if (event.x >= data.middleLeftX
        and event.x <= data.middleRightX
        and event.y >= data.buttonUpperY
        and event.y <= data.buttonLowerY):
            middleThirdClicked(data)

        if (event.x >= data.rightLeftX
        and event.x <= data.rightRightX
        and event.y >= data.buttonUpperY
        and event.y <= data.buttonLowerY):
            rightThirdClicked(data)

    # middle top buttons clicked
    if (event.x >= data.mButtonMiddle - (0.5 * data.mButtonWidth)
    and event.x <= data.mButtonMiddle + (0.5 * data.mButtonWidth)
    and event.y >= data.buttonUpperY - data.thirdHUpper
    and event.y <= data.buttonUpperY - data.thirdHLower):
        middleTopClicked(data)

    #2nd left - sales/YTDmodel - button clicked
    if (event.x >= data.leftButtonLeft
    and event.x <= data.leftButtonRight
    and event.y >= data.buttonUpperY - data.secondHUpper
    and event.y <= data.buttonUpperY - data.secondHLower):
        secondLeftClicked(data)

    #2nd right - export/AllDataModel - button clicked
    elif (event.x >= data.rightButtonLeft
    and event.x <= data.rightButtonRight
    and event.y >= data.buttonUpperY - data.secondHUpper
    and event.y <= data.buttonUpperY - data.secondHLower):
        secondRightClicked(data)

    #3rd left - inventory - button clicked
    elif (event.x >= data.leftButtonLeft
    and event.x <= data.leftButtonRight
    and event.y >= data.buttonUpperY - data.thirdHUpper
    and event.y <= data.buttonUpperY - data.thirdHLower):
        thirdLeftClicked(data)

    #3rd right - vendors - button clicked
    elif (event.x >= data.rightButtonLeft
    and event.x <= data.rightButtonRight
    and event.y >= data.buttonUpperY - data.thirdHUpper
    and event.y <= data.buttonUpperY - data.thirdHLower):
        thirdRightClicked(data)

# takes $ input from user
def keyPressed(event, data):

    if (event.keysym == "1" or event.keysym == "2" or event.keysym == "3" or
        event.keysym == "4" or event.keysym == "5" or event.keysym == "6" or
        event.keysym == "7" or event.keysym == "8" or event.keysym == "9" or
        event.keysym == "0"):
        if data.modelSelect == True:
            data.capital += event.keysym

    if event.keysym == "BackSpace":
        if data.modelSelect == True:
            data.capital = data.capital[:-1]

def timerFired(data):
    pass

## button helpers
####################################

#back button
def leftButtonClicked(data):

    if data.chooseFiles == True:
        data.basis = True
        data.chooseFiles = False

    elif data.modelSelect == True:
        data.chooseFiles = True
        data.modelSelect = False

    elif data.review == True:
        data.modelSelect = True
        data.review = False

    elif data.viewMonth == True:
        data.viewMonth = False
        data.resulting = True

    elif data.viewQuarterly == True:
        data.viewQuarterly = False
        data.resulting = True

    elif data.viewSixMonth == True:
        data.viewSixMonth = False
        data.resulting = True

#next and run buttons
def rightButtonClicked(data):

    if data.chooseFiles == True:
        data.modelSelect = True
        data.chooseFiles = False

    elif data.modelSelect == True:
        data.review = True
        data.modelSelect = False

    elif data.review == True:
        data.runAnimation = True
        data.review = False

    elif (data.viewMonth == True or
        data.viewQuarterly == True or
        data.viewSixMonth == True):
        data.makeCSV = True

#next middle button clicked
def middleBottonClicked(data):
    data.chooseFiles = True
    data.basis = False

#consignment select // show data again button clicked
def middleTopClicked(data):
    if data.modelSelect == True:
        if data.hasConsign == True:
            data.hasConsign = False

        elif data.hasConsign == False:
            data.hasConsign = True

    elif (data.viewMonth == True or
        data.viewQuarterly == True or
        data.viewSixMonth == True):
        data.runTable = True

#button 1 above bottom left button (find sales file / select all data model)
def secondLeftClicked(data):
    if data.chooseFiles == True:
        data.salesPath = findDirectory()
    elif data.modelSelect == True:
        data.model = "All"

#button 1 above bottom right button (pick export folder / select YTD data model)
def secondRightClicked(data):
    if data.chooseFiles == True:
        data.exportPath = saveDirectory()
    elif data.modelSelect == True:
        data.model = "YTD"

#button 2 above bottom left button clicked (pick inventory file)
def thirdLeftClicked(data):
    if data.chooseFiles == True:
        data.inPath = findDirectory()

#button 2 above bottom right button clicked (pick vendor file)
def thirdRightClicked(data):
    if data.chooseFiles == True:
        data.vendorPath = findDirectory()

#left button of 3 on bottom clicked (monthly)
def leftThirdClicked(data):
    data.viewMonth = True
    data.resulting = False

#middle button of 3 on bottom clicked (quarterly)
def middleThirdClicked(data):
    data.viewQuarterly = True
    data.resulting = False

#right button of 3 on bottom clicked (six month)
def rightThirdClicked(data):
    data.viewSixMonth = True
    data.resulting = False

#makes middle button when needed
def createMiddleButtonOther(canvas, data, text, height, fill = None):

    upperY = height
    lowerY = height + data.buttonHeight

    buttonWidth = (data.leftButtonRight - data.leftButtonLeft) * 1.5
    buttonMiddle = (data.leftButtonLeft + data.rightButtonRight) // 2
    buttonLeft = buttonMiddle - buttonWidth // 2
    buttonRight = buttonMiddle + buttonWidth // 2

    canvas.create_rectangle(
    buttonLeft, upperY,
    buttonRight, lowerY,
    fill = fill, width = data.height // 200)

    buttonTextY = (lowerY + upperY) // 2

    canvas.create_text(buttonMiddle, buttonTextY,
    text = text, font = data.font)

#makes more left buttons when needed
def createLeftButtonOther(canvas, data, text, height, fill = None):

    upperY = height
    lowerY = height + data.buttonHeight

    canvas.create_rectangle(
    data.leftButtonLeft, upperY,
    data.leftButtonRight, lowerY,
    fill = fill, width = data.height // 200)

    leftbuttonMid = (data.leftButtonLeft + data.leftButtonRight) // 2
    buttonTextY = (lowerY + upperY) // 2

    canvas.create_text(leftbuttonMid, buttonTextY,
    text = text, font = data.font)

#makes more right buttons when needed
def createRightButtonOther(canvas, data, text, height, fill = None):

    upperY = height
    lowerY = height + data.buttonHeight

    canvas.create_rectangle(
    data.rightButtonLeft, upperY,
    data.rightButtonRight, lowerY,
    fill = fill, width = data.height // 200)

    rightButtonMid = (data.rightButtonLeft + data.rightButtonRight) // 2
    buttonTextY = (lowerY + upperY) // 2

    canvas.create_text(rightButtonMid, buttonTextY,
    text = text, font = data.font)

#makes back/next/run buttons
def makeBackNextButtons(canvas, data, right = "Next", left = "Back"):

    canvas.create_rectangle(
    data.leftButtonLeft, data.buttonUpperY,
    data.leftButtonRight, data.buttonLowerY,
    fill = None, width = data.height // 200)

    leftButtonMid = (data.leftButtonLeft + data.leftButtonRight) // 2
    buttonTextY = (data.buttonUpperY + data.buttonLowerY) // 2

    canvas.create_text(leftButtonMid, buttonTextY,
    text = left, font = data.font)

    canvas.create_rectangle(
    data.rightButtonLeft, data.buttonUpperY,
    data.rightButtonRight, data.buttonLowerY,
    fill = None, width = data.height // 200)

    rightButtonMid = (data.rightButtonLeft + data.rightButtonRight) // 2
    buttonTextY = (data.buttonUpperY + data.buttonLowerY) // 2

    canvas.create_text(rightButtonMid, buttonTextY,
    text = right, font = data.font)

#make left button in bottom 3
def createMiddleLeftButton(canvas, data, text):

    canvas.create_rectangle(
    data.leftLeftX, data.buttonUpperY,
    data.leftRightX, data.buttonLowerY,
    fill = None, width = data.height // 200)

    leftButtonMid = (data.leftLeftX + data.leftRightX) // 2
    buttonTextY = (data.buttonUpperY + data.buttonLowerY) // 2

    canvas.create_text(leftButtonMid, buttonTextY,
    text = text, font = data.smallfont)

#make middle button in bottom 3
def createMiddleMiddleButton(canvas, data, text):

    canvas.create_rectangle(
    data.middleLeftX, data.buttonUpperY,
    data.middleRightX, data.buttonLowerY,
    fill = None, width = data.height // 200)

    middleButtonMid = (data.middleLeftX + data.middleRightX) // 2
    buttonTextY = (data.buttonUpperY + data.buttonLowerY) // 2

    canvas.create_text(middleButtonMid, buttonTextY,
    text = text, font = data.smallfont)

#make right button in bottom 3
def createMiddleRightButton(canvas, data, text):

    canvas.create_rectangle(
    data.rightLeftX, data.buttonUpperY,
    data.rightRightX, data.buttonLowerY,
    fill = None, width = data.height // 200)

    rightButtonMid = (data.rightLeftX + data.rightRightX) // 2
    buttonTextY = (data.buttonUpperY + data.buttonLowerY) // 2

    canvas.create_text(rightButtonMid, buttonTextY,
    text = text, font = data.smallfont)

## make buttons for moe complex screens
####################################

#make buttons on bottom
def makeResultsButtons(canvas, data):

    createMiddleLeftButton(canvas, data, text = "View Monthly")

    createMiddleMiddleButton(canvas, data, text = "View Quarterly")

    createMiddleRightButton(canvas, data, text = "View Six Month")

#makes file select buttons
def makeFileButtons(canvas, data):

    title1 = "Inventory"

    if data.inPath != "":
        fill = "lightGreen"
    else:
        fill = None

    createLeftButtonOther(canvas, data, title1,
    data.buttonUpperY - data.buttonHeight * 3, fill)

    title2 = "Sales"

    if data.salesPath != "":
        fill = "lightGreen"
    else:
        fill = None

    createLeftButtonOther(canvas, data, title2,
    data.buttonUpperY - data.buttonHeight * 1.5, fill)

    title3 = "Vendors"

    if data.vendorPath != "":
        fill = "lightGreen"
    else:
        fill = None

    createRightButtonOther(canvas, data, title3,
    data.buttonUpperY - data.buttonHeight * 3, fill)

    title4 = "Export"

    if data.exportPath != "":
        fill = "lightGreen"
    else:
        fill = None

    createRightButtonOther(canvas, data, title4,
    data.buttonUpperY - data.buttonHeight * 1.5, fill)

#make model select buttons
def makeModelButtons(canvas, data):

    if data.model == "All":
        fillAll = "lightGreen"
        fillYTD = None
    if data.model == "YTD":
        fillAll = None
        fillYTD = "lightGreen"

    title1 = "Use All Data"
    createLeftButtonOther(canvas, data, title1,
    data.buttonUpperY - data.buttonHeight * 1.5, fill = fillAll)

    title2 = "Only YTD Data"
    createRightButtonOther(canvas, data, title2,
    data.buttonUpperY - data.buttonHeight * 1.5, fill = fillYTD)

    title3 = "I have Consignment"

    if data.hasConsign == True:
        fillConsign = "lightGreen"
    else:
        fillConsign = None

    createMiddleButtonOther(canvas, data, title3,
    data.buttonUpperY - data.buttonHeight * 3, fill = fillConsign)

## select file paths
####################################

#prompts user to select .csv file
def findDirectory():
    filename = filedialog.askopenfilename(initialdir = "/",
    title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))

    return filename

#prompts user to select export folder
def saveDirectory():
    savePath = filedialog.askdirectory()

    return savePath

## do things with data
####################################

#run model
def runTKModel(data):

    if data.runAlready == False:

        data.sales = getSales(data.salesPath)
        data.dataPnC = getPnC(data.inPath)
        data.vendors = getVendors(data.vendorPath)
        #remove consigned items if there
        if data.hasConsign == True:
            data.dataPnC = cleanPnC(data.dataPnC, data.vendors)

        data.results = runModel(int(data.capital), data.dataPnC, data.sales,
        data.vendors, data.model, data.exportPath, data.hasConsign)

        data.runAlready = True

#turn output into dataframe, then display table in new tkinter window
def makeDataTable(data, reorderList):

    if data.runTable == True:

        data.df = pd.DataFrame(reorderList, columns = ["SKU", "Vendor", "Name", "Qty"])

        #make new tkinter window - use try/except to minimize chance of crash on scroll
        try:
            sub = Toplevel(data.root)
            sub.title('Table - Scrolling With Trackpad Not Yet Supported!')
            sub.minsize(700, 400)
            sub.maxsize(700, 400)

            pt = Table(sub, dataframe = data.df, showtoolbar = True, showstatusbar = True)
            pt.show()
        except:
            print("Unable to Display - Please Scroll Using Sidebar")

        data.runTable = False

#make csv from specified reorderList
def makeCSV(data, reorderList, model):

    if data.makeCSV == True:

        createCSV(reorderList, data.vendors, model, data.exportPath, data.runCSVcount)
        data.makeCSV = False

        data.runCSVcount += 1

## text
####################################

#makes header for each screen
def makeTitle(canvas, data, title):
    canvas.create_text(
    data.hSplit * data.hSplitR, data.height * 1.5 // data.vSplit,
    text = title, anchor = "e",
    fill = data.mainColor, font = data.bigfont)

#makes main text for each screen
def makeText(canvas, data, text, font):

    canvas.create_text(
    data.hSplit // 2, data.height * 6 // data.vSplit,
    text = text, anchor = "w",
    fill = "black", font = font)

#report results for given model type
def makeResultText(canvas, data, index):

    model = data.results[index][0]
    cost = data.results[index][1]
    expectedRevenue = data.results[index][2]
    expectedProfit = data.results[index][3]
    reorderList = data.results[index][4]

    #make image
    makeResultsImage(canvas, data)

    text = """

    Items Found: %i; Cost to Purchase: $%.2f
    Expected Revenue: $%.2f; Expected Profit: $%.2f
    Scrolling With Trackpad Not Yet Supported in Table!

    """ % (len(reorderList), cost, expectedRevenue, expectedProfit)

    font = data.font
    canvas.create_text(
    data.hSplit // 2 // 2, data.height * 31 // 40,
    text = text, anchor = "w",
    fill = "black", font = font)

    createMiddleButtonOther(canvas, data, "Display Data Again",
    data.buttonUpperY - data.buttonHeight * 3, fill = None)

    #make new tkinter window and display output data
    makeDataTable(data, reorderList)

    #make csv from orderlist when button pressed
    makeCSV(data, reorderList, model)

    makeBackNextButtons(canvas, data, right = "Make CSV")

#make text for results summary screen
def makeSummaryText(canvas, data):

    count = 0

    for modelOut in data.results:

        count += 1

        modelType = modelOut[0]

        if modelType == "YTDMonth" or modelType == "AllMonth":
            model = "next month"
        elif modelType == "YTDQuarter" or modelType == "AllQuarter":
            model = "next quarter"
        elif modelType == "YTDHalf" or modelType == "AllHalf":
            model = "the next six months"

        cost = modelOut[1]
        expectedRevenue = modelOut[2]
        expectedProfit = modelOut[3]
        reorderList = modelOut[4]

        canvas.create_text(data.hSplit // 2,
        (data.height * count // 5) + data.height // 8,

        text = """
        For %s, the model was able to find
        %i items to purchase.
        This allocation would spend $%.2f and generate
        $%.2f in revenue and $%.2f in profit when sold.

        """ % (model, len(reorderList), cost, expectedRevenue, expectedProfit),

        fill = "black", font = data.font, anchor = "w")

## images
####################################

#make image for start page
def makeBasisImage(canvas, data):

    data.photo = PhotoImage(file = "forklift.gif")
    data.photo = data.photo.subsample(3, 3)
    canvas.create_image(data.width * 23 // 32,
    data.height * 15 // 24, image = data.photo)

#make image for runnning page
def makeRunImage(canvas, data):

    data.photo = PhotoImage(file = "forkliftPackage.gif")
    data.photo = data.photo.subsample(4, 4)
    canvas.create_image(data.width * 13 // 24,
    data.height * 2 // 3, image = data.photo)

#make image for runnning page
def makeResultsImage(canvas, data):

    data.photo = PhotoImage(file = "boxes.gif")
    data.photo = data.photo.subsample(7, 7)
    canvas.create_image(data.width * 25 // 48,
    data.height * 7 // 18, image = data.photo)

## draw states
####################################

#draw initial start screen
def drawBasis(canvas, data):

    title = "Reorder What"
    makeTitle(canvas, data, title,)

    text = """

    Welcome to Reorder What, an intelligent system
    that determines what you should purchase for your
    business given each items' profitability and past
    sales history.

    Start by placing your data
    into the template file
    following the example
    offered. Save each sheet
    as a CSV UTF-8 file.

    """
    makeText(canvas, data, text, font = data.biggerfont)

    makeBasisImage(canvas, data)

    title3 = "Next"

    createMiddleButtonOther(canvas, data, title3,
    data.buttonUpperY)

    #makeBackNextButtons(canvas, data, right = "Other", left = "QuickBooks")

#draw choose file screen
def drawChooseFiles(canvas, data):

    title = "Choose Files"
    makeTitle(canvas, data, title)

    text = """
    Now, select the location of your data files and the folder
    where you would like the resulting files to be saved.

    You currently have selected:
    "%s" for inventory
    "%s" for sales
    "%s" for vendors
    and "%s" for export







    """ % (data.inPath, data.salesPath, data.vendorPath, data.exportPath)

    makeText(canvas, data, text, font = data.smallfont)

    makeFileButtons(canvas, data)

    makeBackNextButtons(canvas, data)

#draw model type / allocate $ screen
def drawModelSelect(canvas, data):

    title = "Spend + Model"
    makeTitle(canvas, data, title)

    text = """

    Type to specify the amount you'd like the program to spend.
    Press backspace to delete

    Amount = $%s

    Now, select if you have consigned goods and how much data
    you would like the model to use.






    """ % (data.capital)

    makeText(canvas, data, text, font = data.font)

    makeModelButtons(canvas, data)

    makeBackNextButtons(canvas, data)

#draw summary of user input screen (before run)
def drawReview(canvas, data):

    title = "Review"
    makeTitle(canvas, data, title)

    if data.model == "YTD":
        dataType = "data for this year"
    elif data.model == "All":
        dataType = "all available data"

    if data.hasConsign == True:
        consignment = "has"
    elif data.hasConsign == False:
        consignment = "does not have"


    text = """

    Your file that tracks inventory is located at:
    %s

    Your file that tracks sales is located at:
    %s

    Your file that tracks vendor information is located at:
    %s

    You are allocating $%s using %s.
    Your data %s consignment goods.

    All of this will be exported to:
    %s

    """ % (data.inPath, data.salesPath, data.vendorPath,
    data.capital, dataType, consignment, data.exportPath)

    makeText(canvas, data, text, font = data.font)

    makeBackNextButtons(canvas, data, right = "Run")

#draw running screen
def drawRun(canvas, data):

    title = "Running"
    makeTitle(canvas, data, title)

    canvas.create_text(data.width // 2, data.height // 3,
    text = "Pulling Results from the Warehouse", fill = "black", font = data.muchbigger)

    makeRunImage(canvas, data)

#draw result summary screen
def drawResults(canvas, data):

    data.runTable = True

    title = "Results"
    makeTitle(canvas, data, title)

    makeSummaryText(canvas, data)

    makeResultsButtons(canvas, data)

#draw result for month model screen
def drawMonth(canvas, data):
    title = "Month Results"
    makeTitle(canvas, data, title)

    #report data based on model index in list
    index = 0
    makeResultText(canvas, data, index)

#draw result for quarter model screen
def drawQuarter(canvas, data):
    title = "Quarter Results"
    makeTitle(canvas, data, title)

    #report data based on model index in list
    index = 1
    makeResultText(canvas, data, index)

#draw result for 6 month model screen
def drawSixMonth(canvas, data):
    title = "Six Month Results"
    makeTitle(canvas, data, title)

    #report data based on model index in list
    index = 2
    makeResultText(canvas, data, index)

#control which screen is displayed
def drawBackground(canvas, data):

    if data.basis == True:
        drawBasis(canvas, data)
    elif data.chooseFiles == True:
        drawChooseFiles(canvas, data)
    elif data.modelSelect == True:
        drawModelSelect(canvas, data)
    elif data.review == True:
        drawReview(canvas, data)
    elif data.actualRun == True:
        runTKModel(data)
        data.runAnimation = False
        data.actualRun = False
        data.resulting = True
    elif data.runAnimation == True:
        drawRun(canvas, data)
        data.actualRun = True
    elif data.resulting == True:
        drawResults(canvas, data)
    elif data.viewMonth == True:
        drawMonth(canvas, data)
    elif data.viewQuarterly == True:
        drawQuarter(canvas, data)
    elif data.viewSixMonth == True:
        drawSixMonth(canvas, data)

def redrawAll(canvas, data):
    drawBackground(canvas, data)

####################################
# also from 15-112 website
# same except made root an element of data to run table window
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
        fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    data.root = Tk()

    canvas = Canvas(data.root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    data.root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    data.root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    data.root.mainloop()  # blocks until window is closed

    print("bye!")

run(600, 600)
