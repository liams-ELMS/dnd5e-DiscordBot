# Use 'pip install discord.py' in the shell to install discord.py
# Use 'python main.py' in the shell to run this
import discord
from discord.ext import commands
from urllib.request import urlopen
import json
import random

def grabLink(strAddition):
  # Use urlopen and json to turn a link to the api into a usable dictionary
  strURL = "https://www.dnd5eapi.co" + strAddition
  strURL = urlopen(strURL)
  strURL = strURL.read()
  dctURL = json.loads(strURL)
  return dctURL
#~~~~~end !grabLink~~~~~#

def main():
  # Sets up bot
  intents = discord.Intents.default()
  intents.members = True
  intents.message_content = True
  
  bot = commands.Bot(command_prefix='!', intents=intents)

  @bot.event
  async def on_ready():
    # Prints messages in python log of what servers the bot is connected too and sends a message in discord to let everyone know it is runnin
    print(f"Logged in as {bot.user.name}")
    print("Connected to the following servers:")
    # O = n
    for guild in bot.guilds:
      print(f"- {guild.name}")
    general_channel = bot.get_channel() # Needs a Channel Code to work!
    await general_channel.send('Hello, world! Type !help for my commands!')
      
  @bot.event
  async def on_message(message):
    # Creates a log in the python output of all messages
    if bot.user == message.author:
      return
    if not message.channel.permissions_for(message.guild.me).read_messages:
      return
    print(f"Received message: {message.content}")
    # Reads commands from messages
    await bot.process_commands(message)
  
  @bot.command(brief="Get information about the classes", description="Use '!classes' to get a list of the classes or use '!classes <class>' to get more details on a specific class (Replace <class> with a class from the list).")
  async def classes(ctx):
    # Grab the command the user sent
    strMessage = ctx.message.content
    lstMessage = strMessage.split(" ", 1)

    # Create a string to be filled out and printed out
    strOutput = ""
    
    # If user typed in command with class
    # Return details of the class
    if len(lstMessage) == 2:
      # add the class user asked for to url and open it
      try:
        dctURL = grabLink("/api/classes/" + lstMessage[1].lower())
      # Return an error incase they entered an invalid class
      except:
        strOutput = "Class not found. Type in '!classes' for a list of valid options"
      else:
        # Create the output
        strOutput += f"**Class**: {dctURL['name']}\n"
        strOutput += f"**Hit Die**: d{dctURL['hit_die']}\n"
    
        # Create a list of skills (O = n)
        strTempOutput = ""
        for x in dctURL['proficiency_choices'][0]['from']['options']:
          strProf = x['item']['name']
          lstProf = strProf.split(" ", 1)
          if lstProf[0] == "Skill:":
            if strTempOutput == "":
              strTempOutput += f"{lstProf[1]}"
            else:
              strTempOutput += f", {lstProf[1]}"
    
        # Create the output
        strOutput += f"**Skills (Choose {dctURL['proficiency_choices'][0]['choose']})**: {strTempOutput}\n"
        
        # Create a list of proficiencies (O = n)
        strTempOutput = ""
        for x in dctURL['proficiencies']:
          if ":" not in x['name']:
            if strTempOutput == "":
              strTempOutput += f"{x['name']}"
            else:
              strTempOutput += f", {x['name']}"
  
        # Create the output
        strOutput += f"**Proficiencies**: {strTempOutput}\n"
  
        # Create a list of tools if class has them
        strTempOutput = ""
        if len(dctURL['proficiency_choices']) == 1:
          strTempOutput = "None"
        else:
          strTempOutput += dctURL['proficiency_choices'][1]['desc']
          
        # Create the output
        strOutput += f"**Tools**: {strTempOutput}\n"
        strOutput += f"**Saving Throws**: {dctURL['saving_throws'][0]['name']} & {dctURL['saving_throws'][1]['name']}\n"
  
        # Open a new URL to see the classes unique abilities
        dctURL = grabLink(dctURL['class_levels'])

        # Create the output
        strOutput += "**Features**:"  
        # Create the list of features (O = n^2)
        for feature in dctURL:
          strOutput += f" *Level {feature['level']}*: "
          strTempOutput = ""
          for x in feature['features']:
            if strTempOutput == "":
              strTempOutput += f"{x['index'].replace('-', ' ').title()}"
            else:
              strTempOutput += f", {x['index'].replace('-', ' ').title()} "
          strOutput += strTempOutput
      
    # If user typed in command without a class
    # Return all of the possible classes
    else:
      # Open base URL and list out the classes
      dctURL = grabLink("/api/classes/")
      strOutput += "**Classes**: "
      # O = n
      for x in dctURL['results']:
        if strOutput == "**Classes**: ":
          strOutput += f"{x['name']}"
        else:
          strOutput += f", {x['name']}"
    if strOutput != "":
      print("Returned Output")
      await ctx.send(strOutput)
  #~~~~~END !classes~~~~~#

  @bot.command(brief="Get information about a specific feature", description="Use '!features <feature>' to get more details on a specific feature. You can get a list of features from each class by using the '!classes <class>' command.")
  async def features(ctx):
    # Grab the command the user sent
    strMessage = ctx.message.content
    lstMessage = strMessage.split(" ", 1)

    # Create a string to be filled out and printed out
    strOutput = ""

    # If user typed in command with class
    # Return details of the class
    if len(lstMessage) == 2:
      strInput = lstMessage[1].replace(" ", "-")
      try:
        dctURL = grabLink("/api/features/" + strInput.lower())
      except:
        strOutput = "Feature not found. Gain a list of features from a specific class, use the '!classes <class>' command."
      else:
        strOutput = f"**Feature**: {dctURL['name']}\n**Class**: Level {dctURL['level']} {dctURL['class']['name']}\n**Description**: {dctURL['desc'][0]}"

    # If user typed in command without a feature
    # Return all of the possible classes
    else:
      strOutput = "Please type in a feature with the command. You can get a list of features from each class by using the '!classes <class>' command."

    if strOutput != "":
      print("Returned Output")
      await ctx.send(strOutput)
#~~~~~END !features~~~~~#
  
  @bot.command(brief="Get information about the races", description="Use '!races' to get a list of the races or use '!races <race>' to get more details on a specific class (Replace <race> with a race from the list).")
  async def races(ctx):
    # Grab the command the user sent
    strMessage = ctx.message.content
    lstMessage = strMessage.split(" ", 1)

    # Create a string to be filled out and printed out
    strOutput = ""
    
    if len(lstMessage) == 2:
      # add the class user asked for to url and open it
      try:
        dctURL = grabLink("/api/races/" + lstMessage[1].lower())
      # Return an error incase they entered an invalid class
      except:
        strOutput = "Race not found. To get a list of valid races, use the !races command."
      else:
        # Create the output
        strOutput += f"**Race**: {dctURL['name']}\n"
        strOutput += f"**Movement Speed**: {dctURL['speed']} ft\n"
    
        # Create the output (with a loop)
        strOutput += "**Ability Bonuses**:"
        # O = n
        for x in dctURL['ability_bonuses']:
          strOutput += f" {x['ability_score']['name']} +{x['bonus']}"

        # Create the output
        strOutput += f"\n**Size**: {dctURL['size']}\n"

        # Create the output
        strTempOutput = ""
        # O = n
        for x in dctURL['languages']:
          if strTempOutput == "":
            strTempOutput += f"{x['name']}"
          else:
            strTempOutput += f", {x['name']}"

        strOutput += f"**Languages**: {strTempOutput}\n"

        # Create the output
        strTempOutput = ""
        # O = n
        for x in dctURL['traits']:
          if strTempOutput == "":
            strTempOutput += f"{x['index'].replace('-', ' ').title()}"
          else:
            strTempOutput += f", {x['index'].replace('-', ' ').title()}"

        strOutput += f"**Traits**: {strTempOutput}\n"

        # Create the output
        strTempOutput = ""
        if len(dctURL['subraces']) != 0:
          # O = n
          for x in dctURL['subraces']:
            if strTempOutput == "":
              strTempOutput += f"{x['name']}"
            else:
              strTempOutput += f", {x['name']}"
        else:
          strTempOutput = "N/A"

        strOutput += f"**Subraces**: {strTempOutput}"
        
    # If user typed in command without a class
    # Return all of the possible classes
    else:
      # Open base URL and list out the classes
      dctURL = grabLink("/api/races/")
      strOutput += "**Races**: "
      # O = n
      for x in dctURL['results']:
        if strOutput == "**Races**: ":
          strOutput += f"{x['name']}"
        else:
          strOutput += f", {x['name']}"
      
    if strOutput != "":
      print("Returned Output")
      await ctx.send(strOutput)
#~~~~~End !races~~~~~#

  @bot.command(brief="Get information about a specific trait", description="Use '!traits <trait>' to get more details on a specific trait. You can get a list of traits from each race by using the '!races <race>' command.")
  async def traits(ctx):
    # Grab the command the user sent
    strMessage = ctx.message.content
    lstMessage = strMessage.split(" ", 1)

    # Create a string to be filled out and printed out
    strOutput = ""

    # If user typed in command with class
    # Return details of the class
    if len(lstMessage) == 2:
      strInput = lstMessage[1].replace(" ", "-")
      try:
        dctURL = grabLink("/api/traits/" + strInput.lower())
      except:
        strOutput = "Trait not found. To get a list of traits from a race, use '!races <race>' and look for the Traits section."
      else:
        # Create the output
        strOutput += f"**Trait**: {dctURL['name']}\n"
        
        # Create the output (with a loop)
        strTempOutput = ""
        # O = n
        for x in dctURL["races"]:
          if strTempOutput == "":
            strTempOutput += f"{x['name']}"
          else:
            strTempOutput += f", {x['name']}"
        
        # Create the output
        strOutput += f"**Race(s)**: {strTempOutput}\n"
        strOutput += f"**Description**: {dctURL['desc'][0]}"

    # If user typed in command without a feature
    # Return all of the possible classes
    else:
      strOutput = "Please type in a trait with the command. You can get a list of traits from each race by using the '!races <race>' command."

    if strOutput != "":
      print("Returned Output")
      await ctx.send(strOutput)
#~~~~~END !traits~~~~~#

  @bot.command(brief="Get information about a specific spell", description="Use '!spells <letter>' to get a list of spells that start with that letter. You can get the details of a specific spell by using '!spells <spell>' (Replace <spell> with a spell from the list).")
  async def spells(ctx):
    # Grab the command the user sent
    strMessage = ctx.message.content
    lstMessage = strMessage.split(" ", 1)

    # Create a string to be filled out and printed out
    strOutput = ""

    # Find the spell the user inputed
    if len(lstMessage) == 2 and len(lstMessage[1]) > 1:
      # add the spell user asked for to url and open it
      strInput = lstMessage[1].replace(" ", "-")
      try:
        dctURL = grabLink("/api/spells/" + strInput.lower())
      # Return an error incase they entered an invalid spell
      except:
        strOutput = "Spell not found. To get a list of spells that start with a specific letter, use '!spells <letter>'"
      else:
        # Create the output
        strOutput += f"**Spell**: {dctURL['name']}\n"
        strOutput += f"*Level {dctURL['level']} {dctURL['school']['name']} spell*\n"
        strOutput += f"**Casting Time**: {dctURL['casting_time']}\n"
        strOutput += f"**Range**: {dctURL['range']}\n"
        # Create the output (with a loop)
        strTempOutput = ""
        # O = n
        for x in dctURL["components"]:
          if strTempOutput == "":
            strTempOutput += f"{x}"
          else:
            strTempOutput += f", {x}"
        try:
          strOutput += f"**Components**: {strTempOutput} ({dctURL['material']})\n"
        except:
          strOutput += f"**Components**: {strTempOutput}\n"
        strOutput += f"**Duration**: {dctURL['duration']}\n"
        strOutput += f"**Concentration**: {dctURL['concentration']}\n"
        strOutput += f"**Ritual**: {dctURL['ritual']}\n"
        # Create the output (with a loop)
        # O = n
        for x in dctURL["desc"]:
            strOutput += f"\t{x}\n"
        # O = n
        for x in dctURL["higher_level"]:
            strOutput += f"\t{x}\n"

    # List all spells that start with the letter the user inputed
    elif len(lstMessage) == 2 and len(lstMessage[1]) == 1:
      dctURL = grabLink("/api/spells/")
      strOutput = f"**Spells that start with {lstMessage[1][0].upper()}**: "
      # O = n
      for x in dctURL['results']:
        if x['index'][0] == lstMessage[1][0].lower():
          if strOutput == f"**Spells that start with {lstMessage[1][0].upper()}**: ":
            strOutput += f"{x['index'].replace('-', ' ').title()}"
          else:
            strOutput += f", {x['index'].replace('-', ' ').title()}"

    # Ask user for a spell name or a letter
    else:
      strOutput = "To use !spells, please put in a spell name after the command. Alternatively, if you put in a single letter, this command will return all spells that start with that letter."

    print("Returned Output")
    await ctx.send(strOutput)
#~~~~~End !spells~~~~~#

  @bot.command(brief="Get information about specific equipment", description="Use '!equipment <letter>' to get a list of equipment that starts with that letter. You can get the details of specific equipment by using '!equipment <item>' (Replace <item> with equipment from the list).")
  async def equipment(ctx):
    # Grab the command the user sent
    strMessage = ctx.message.content
    lstMessage = strMessage.split(" ", 1)

    # Create a string to be filled out and printed out
    strOutput = ""

    # Find the equipment the user inputed
    if len(lstMessage) == 2 and len(lstMessage[1]) > 1:
      strInput = lstMessage[1].replace(" ", "-")
      # add the equipment user asked for to url and open it
      try:
        dctURL = grabLink("/api/equipment/" + strInput.lower())
      # Return an error incase they entered an invalid equipment
      except:
        strOutput = "Equipment not found. To get a list of equipment that start with a specific letter, use !equipment <letter>"
      else:
        # Create the output
        strOutput += f"**Name**: {dctURL['name']}\n"
        strOutput += f"**Category**: {dctURL['equipment_category']['name']}\n"

        # Create different output based on category
        if dctURL['equipment_category']['index'] == "weapon":
          strOutput += f"**Type**: {dctURL['category_range']}\n"
          strOutput += f"**Damage**: {dctURL['damage']['damage_dice']} {dctURL['damage']['damage_type']['name']}\n"
          try:
            strOutput += f"**Range**: {dctURL['range']['normal']}/{dctURL['range']['long']} ft\n"
          except:
            strOutput += f"**Range**: {dctURL['range']['normal']} ft\n"
          strTempOutput = ""
          # O = n
          for x in dctURL["properties"]:
            if strTempOutput == "":
              strTempOutput += f"{x['name']}"
            else:
             strTempOutput += f", {x['name']}"
          strOutput += f"**Properties**: {strTempOutput}\n"
        
        elif dctURL['equipment_category']['index'] == "armor":
          strOutput += f"**Type**: {dctURL['armor_category']} Armor\n"
          strOutput += f"**Armor Class**: {dctURL['armor_class']['base']}\n"
          strOutput += f"**STR Required**: {dctURL['str_minimum']} STR\n"
          strOutput += f"**Disadvantage on Stealth**: {dctURL['stealth_disadvantage']}\n"
        
        # Create the output
        strOutput += f"**Cost**: {dctURL['cost']['quantity']} {dctURL['cost']['unit']}\n"
        strOutput += f"**Weight**: {dctURL['weight']} lbs\n"

    # List all equipment that start with the letter the user inputed
    elif len(lstMessage) == 2 and len(lstMessage[1]) == 1:
      dctURL = grabLink("/api/equipment/")
      strOutput = f"**Equipment that start with {lstMessage[1][0].upper()}**: "
      # O = n
      for x in dctURL['results']:
        if x['index'][0] == lstMessage[1][0].lower():
          if strOutput == f"**Equipment that start with {lstMessage[1][0].upper()}**: ":
            strOutput += f"{x['index'].replace('-', ' ').title()}"
          else:
            strOutput += f", {x['index'].replace('-', ' ').title()}"

    # Ask user for a equipment name or a letter
    else:
      strOutput = "To use !equipment, please put in the name of the equipment after the command. Alternatively, if you put in a single letter, this command will return all equipment that starts with that letter."

    print("Returned Output")
    await ctx.send(strOutput)
#~~~~~end !equipment~~~~~#

  @bot.command(brief="Roll some dice", description="Type the command like '!roll XdY'. Replace X with the amount of dice and replace Y with the amount of sides on the dice. For example use 1d20 to roll a twenty sided dice or 8d6 to roll 8 six sided dice.")
  async def roll(ctx):
    strMessage = ctx.message.content
    lstMessage = strMessage.split(" ", 1)
    strOutput = ""
    if len(lstMessage) == 2:
      lstDice = lstMessage[1].split("d")
      try:
        # O = n
        for x in range(0, int(lstDice[0])):
          strOutput += f"{random.randint(1, int(lstDice[1]))} "
      except:
        strOutput = "Incorrect syntax. Type the command as '!roll XdY'. Replace X with the amount of dice and replace Y with the amount of sides on the dice."
    else:
      strOutput = "Type the command like '!roll XdY'. Replace X with the amount of dice and replace Y with the amount of sides on the dice. For example use 1d20 to roll a twenty sided dice or 8d6 to roll 8 six sided dice."
        
    print("Returned Output")
    await ctx.send(strOutput)
#~~~~~End !roll~~~~~#

  # Runs the bot
  bot.run() #Need a Discord Bot Token Here!

#~~~~~End main()~~~~~#

main()