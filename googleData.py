import gspread
from google.oauth2.service_account import Credentials
from sms import formatPhoneNumber


class googleSheet():
    def __init__(self):
        googleSheetID = "1vXwuRM1cqyithCI8MUfRAENMdLwKwuKsswM1XwF0BSA"
        # Define the scope
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

        # Load the credentials
        tokenPath = r"..\secrets\token.json"
        creds = Credentials.from_service_account_file(tokenPath, scopes=SCOPES)

        # Authorize with gspread
        client = gspread.authorize(creds)

        # Open the Google Sheet by ID
        sheet = client.open_by_key(googleSheetID)

        # Select the first worksheet
        self.worksheet = sheet.get_worksheet(0)

    def pullStoryInfo(self, phoneNumber):


        self.userInfo = {
            "GS Row Index" : "error",
            "From Number" : phoneNumber.lower(),
            "Story Path" : "error",
            "Milestone" : "error",
            "Promo Code Win": "error",
            "Promo Code Lose": "error"
        }

        def formatToString(googleSheetValueList):
            return [list(x)[0] for x in googleSheetValueList]

        storyMilestones = formatToString(self.worksheet.get("C2:C"))
        storyPaths = formatToString(self.worksheet.get("B2:B"))
        fromNumbers = formatToString(self.worksheet.get("A2:A"))
        promoCodeWins = formatToString(self.worksheet.get("D2:D"))
        promoCodeLoses = formatToString(self.worksheet.get("E2:E"))

        userInfoFound = False
        for index in range(0,len(fromNumbers)):
            value = fromNumbers[index]
            if phoneNumber == value:
                self.userInfo["GS Row Index"] = index+2
                self.userInfo["Story Path"] = storyPaths[index].lower()
                self.userInfo["Milestone"] = storyMilestones[index].lower()
                self.userInfo["Promo Code Win"] = promoCodeWins[index]
                self.userInfo["Promo Code Lose"] = promoCodeLoses[index]
                userInfoFound = True


        if userInfoFound == False:
            self.userInfo["GS Row Index"] = len(fromNumbers)+2
            self.worksheet.update(f'A{self.userInfo["GS Row Index"]}', [[f"{self.userInfo["From Number"]}"]])
            self.worksheet.update(f'B{self.userInfo["GS Row Index"]}', [[f"none"]])
            self.worksheet.update(f'C{self.userInfo["GS Row Index"]}', [[f"none"]])

            self.userInfo["Story Path"] = "none"
            self.userInfo["Milestone"] = "none"
            self.userInfo["Promo Code Win"] = promoCodeWins[len(fromNumbers)+2+1]
            self.userInfo["Promo Code Lose"] = promoCodeLoses[len(fromNumbers)+2+1]
        return self.userInfo


    def updateGoogleSheet(self, phone="same", storyPath="same", milestone="same"):
        if phone != "same":
            self.worksheet.update(f'A{self.userInfo["GS Row Index"]}', [[f"{phone}"]])
        if storyPath != "same":
            self.worksheet.update(f'B{self.userInfo["GS Row Index"]}', [[f"{storyPath}"]])
        if milestone != "same":
            self.worksheet.update(f'C{self.userInfo["GS Row Index"]}', [[f"{milestone}"]])
        return True

