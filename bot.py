import random
import time
from googleData import googleSheet
from sms import sendSMS, TESTsendSMS, formatPhoneNumber
import re
from sendEmail import sendEmail
import traceback
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    startTime = time.time()
    #<--------------------------------SETUP AND LOAD------------------------------------------------------------->
    try:
        # collect message data from twilio
        userInput = request.values.get('Body', '').lower()
        fromTelephoneNumber = request.values.get('From', '')
        resp = MessagingResponse()
        msg = resp.message()
        responded = False



        # for testing
        # fromTelephoneNumber = formatPhoneNumber("(US) +1 253 219 2704")
        # userInput = input("enter input\n")



        userInput = cleaned = re.sub(r'[^A-Za-z0-9]', '', userInput).lower()
        gs = googleSheet()
        gs.pullStoryInfo(fromTelephoneNumber)



        if userInput == "stop":
            gs.updateGoogleSheet(storyPath="stop", milestone="stop")


        #<--------------------------------DEFINE ADVENTURES------------------------------------------------------------->
        def adventure1(userInput):

            if userInput == "adventure1":
                return """
        Thanks for playing this space text adventure. Reply with STOP at any time to unsubscribe from all messages. 
    
        You've received a mysterious distress signal from an ancient starship, the Stellar Whisper, long thought lost near the glittering moon of Luminara. Your mission is to explore the ship, recover any valuable data or artifacts, and if possible unlock the Vault of Luminara, rumored to hold lost knowledge of advanced hyperspace technology.
    
        ARRIVAL ON THE SHIP
    
        The airlock hisses open. A dim blue light pulses along the floor of the Stellar Whisper’s corridor. You hear the faint hum of emergency systems and a crackle from an old speaker.
    
        **Do you:**
    
        1. Walk straight toward the bridge(reply BRIDGE)
        2. Head left toward the crew quarters(reply QUARTERS)
        3. Turn right toward the science bay(reply SCIENCE)
        """ #start



            if userInput == "bridge":
                gs.updateGoogleSheet(milestone="bridge")
                return """
        **Bridge**:
    
        You enter the bridge. The chairs are empty, floating slightly due to faulty gravity. A console flickers with a prompt:
    
        **“LAST COMMAND ENTERED: VAULT LOCK INITIATED. PASSWORD REQUIRED.”**
    
        Next to it, a note scrawled on a datapad reads: “The captain said the stars know the truth. But I think it’s a trick…” You now have a clue: "Stars know the truth" might relate to the password
    
        **Do you:**
    
        1. Search the room(reply SEARCH)
        2. Enter the Password into the vault(reply with the password)
        3. Head toward the crew quarters(reply QUARTERS)
        4. Turn toward the science bay(reply SCIENCE)
        """ # go to bridge


            if userInput == "science":
                gs.updateGoogleSheet(milestone="science")
                return """
        This lab is better lit, but eerie. Screens display old data on the moon Luminara. 
    
        **Do you:**
    
        1. Search the room(reply SEARCH)
        2. Head toward the crew quarters(reply QUARTERS)
        3. Turn toward the bridge(reply BRIDGE)
        4. Continue through the lab to the medbay(reply MEDBAY)
        """ #go to science bay, continue to medbay

            if userInput == "quarters":
                gs.updateGoogleSheet(milestone="quarters")
                return """
        Dust drifts in the stale air. Personal items are still scattered: a model starship, a cracked photo of the crew, and a holo-recording device.
    
        **Do you:**
    
        1. Search the rooms(reply SEARCH)
        2. Turn toward the science bay(reply SCIENCE)
        3. Head toward the bridge(reply BRIDGE)
        """ #go to quarters


            if userInput == "medbay":
                gs.updateGoogleSheet(milestone="medbay")
                return """
        The medbay is sterile and quiet. A single cot lies in the corner.
    
        **Do you:**
    
        1. Search the room(reply SEARCH)
        2. Head back the science bay(reply SCIENCE)
        """ #go to medbay


            if gs.userInfo["Milestone"] == "bridge":
                if userInput == "luminadark9":
                    gs.updateGoogleSheet(milestone="finish")
                    return f'The console hums. Lights flicker… and then a shimmering door at the back of the bridge slides open!\n\nInside lies a glowing orb surrounded by drift crystals, and a datachip labeled: “To the brave who trusted their mind more than their eyes.” The datachip reveals blueprints for a new Drift Engine, one that doesn’t require fuel. Your name will be remembered.\n\n**YOU WIN!** 🎉\nYou found the real password and opened the Vault of Luminara.\nThanks for playing, Order online with Westside Pizza in Buckley to get a free order of cheese stix with promo code {gs.userInfo["Promo Code Lose"]}' #correct pw
                elif userInput == "search":
                    return """
        You activate the star chart. Constellations swirl in holographic form.
    
        A blinking label reads: “Captain’s Code: NOVA-RAY7” """#star charts
                else:
                    return """
        The console beeps three times. A red light flashes.
    
        **"ACCESS DENIED. SIMULATED CODE ENGAGED. NICE TRY."**
    
        A message appears: “Captain Ellira: If you trusted the stars, you didn’t trust me. Try again.” """#wrong pw

            if gs.userInfo["Milestone"] == "science":
                if userInput == "search":
                    return """
        Screens display old data on the moon Luminara. One file blinks: “Personal Logs – Captain Ellira”. You open it: “Final log. I’ve locked the vault. The real code is in the place no stars shine. Just like the vault—deep and hidden.”
        """#personal logs for captain

            if gs.userInfo["Milestone"] == "quarters":
                if userInput == "search":
                    return """You press play on the holo-recording.
    
        > “Captain Ellira always loved riddles. She left the real code somewhere safe—but made up a fake one too, hidden in the constellations. Said she wanted to ‘test our minds.’ I just hope someone remembers where she put the real one…” """#holo recording

            if gs.userInfo["Milestone"] == "medbay":
                if userInput == "search":
                    return """You crouch and look underneath the cot. There’s a scratched message:
    
        “vault key: LUMINA-DARK9”
    
        You jot it down."""#scrawled note under the cot


            return """Invalid Input Message. If you are stuck, you can reply ADVENTURE1 to restart"""

        def marketing1(userInput):


            def lettersOnly(string):
                return ''.join(c for c in userInput if c.isalpha())

            def numbersOnly(string):
                return ''.join(c for c in userInput if c.isdigit())

            if gs.userInfo["Milestone"] != "finish":

                if userInput == "marketing1":
                    return """
            🎲 Ready to play? Reply with one of these commands to test your luck for a chance to win a FREE PIZZA!
            **Do you:**
    
            1. Guess the total of 2 dice rolls(reply ROLL)
            2. Flip a coin 3 times. Get heads three times to win(reply COIN)
            3. Choose a number between 1 and 20 and see if you hit the mark(reply PICK)
            """ #start



                if userInput == "roll":
                    gs.updateGoogleSheet(milestone="roll")
                    return f"Rolling two 6-sided dice....Guess the number"

                if gs.userInfo["Milestone"] == "roll":
                    dice1 = int(random.randint(1,6))
                    dice2 = int(random.randint(1,6))
                    winningNumber = dice1+dice2
                    gs.updateGoogleSheet(milestone="finish")
                    if int(numbersOnly(userInput)) == int(winningNumber):
                        return f"dice 1: {dice1}\ndice 2: {dice2}\n**YOU WIN!** 🎉\nUse Promo Code {gs.userInfo["Promo Code Win"]} when you order online with Westside Pizza Buckley for a FREE Medium 2-Topping Pizza!"
                    else:
                        return f"dice 1: {dice1}\ndice 2: {dice2}\nClose call, but not a win this time...\nNo worries — you're still a winner in our book!\nEnjoy a FREE order of cheese stix on us.\n\nUse Promo Code {gs.userInfo["Promo Code Lose"]} when you order online.\nThanks for playing\n"



                if userInput == "coin":
                    possibleCoinFacing = ["Heads", "Tails"]
                    coin1 = random.choice(possibleCoinFacing)
                    coin2 = random.choice(possibleCoinFacing)
                    coin3 = random.choice(possibleCoinFacing)
                    gs.updateGoogleSheet(milestone="finish")
                    if coin1 == "Heads" and coin2 == "Heads" and coin3 == "Heads":
                        winLoseMessage = f"CONGRATS! You Win!\nUse Promo Code {gs.userInfo["Promo Code Win"]} for a free medium 2-topping pizza when you order online"
                    else:
                        winLoseMessage = f"Close call, but not a win this time...\nNo worries — you're still a winner in our book!\nEnjoy a FREE order of cheese stix on us.\n\nUse Promo Code {gs.userInfo["Promo Code Lose"]} when you order online.\nThanks for playing\n"
                    return f"Readying Coin flipper....\nCoin 1: {coin1}\nCoin 2: {coin2}\nCoin 3: {coin3}\n\n{winLoseMessage}"


                if userInput == "pick":
                    gs.updateGoogleSheet(milestone="pick")
                    return "Setting up our Random Number Generator....guess a number between 1 and 20"

                if gs.userInfo["Milestone"] == "pick":
                    random1 = int(random.randint(1,20))
                    random2 = int(random.randint(1,20))
                    while random1 == random2:
                        random2 = int(random.randint(1, 20))
                    gs.updateGoogleSheet(milestone="finish")
                    if int(numbersOnly(userInput)) == int(random1) or int(numbersOnly(userInput)) == int(random2):
                        return f"The Lucky numbers were...{random1} & {random2}\n**YOU WIN!** 🎉\nUse Promo Code {gs.userInfo["Promo Code Win"]} when you order online with Westside Pizza Buckley for a FREE Medium 2-Topping Pizza!"
                    else:
                        return f"The Lucky numbers were...{random1} & {random2}\nClose call, but not a win this time...\nNo worries — you're still a winner in our book!\nEnjoy a FREE order of cheese stix on us.\n\nUse Promo Code {gs.userInfo["Promo Code Lose"]} when you order online.\nThanks for playing\n"


                return """Thanks for reaching out to Westside Pizza in Buckley. This phone number is automated and not monitored. For assistance reach out to us at (360) 829-0800. Reply STOP to unsubscribe."""
            else:
                return "Thanks for playing"
        #<--------------------------------RUN ADVENTURES------------------------------------------------------------->
        if userInput != "stop" or gs.userInfo["Story Path"] != "stop":
            if userInput == "adventure1":
                gs.updateGoogleSheet(storyPath="adventure1", milestone="start")
                gs.pullStoryInfo(fromTelephoneNumber)
                message = adventure1(userInput)

            if userInput == "marketing1":
                gs.updateGoogleSheet(storyPath="marketing1", milestone="start")
                gs.pullStoryInfo(fromTelephoneNumber)
                message = marketing1(userInput)

            # if user didnt start a new story, check which story they are on

            if gs.userInfo["Story Path"] == "adventure1":
                message = adventure1(userInput)

            if gs.userInfo["Story Path"] == "marketing1":
                message = marketing1(userInput)


        #<--------------------------------SEND REPLY TEXT------------------------------------------------------------->
        if "message" in locals():
            # sendSMS(fromTelephoneNumber, message=message)
            msg.body(message)
            responded = True
        else:
            message = "Thanks for reaching out to Westside Pizza in Buckley. This phone number is automated and not monitored. For assistance reach out to us at (360) 829-0800. Reply STOP to unsubscribe."
            # sendSMS(fromTelephoneNumber, message=message)
            msg.body(message)
            responded = True


    except Exception as e:
        timeDiff = round((time.time()-startTime)/60, 2)
        sendEmail("kylegrote@westsidepizza.com", f"An error occurred in {__file__}:", f"{e}\n{traceback.print_exc()}\nProcess ran for {timeDiff} minutes")



    return str(resp)


if __name__ == '__main__':
    app.run()


