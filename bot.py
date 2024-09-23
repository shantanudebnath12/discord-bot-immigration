import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Remove the default help command
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')

@bot.event
async def on_member_join(member):
    welcome_channel = member.guild.system_channel  # Or specify a channel ID
    if welcome_channel is not None:
        welcome_message = f"""Welcome {member.mention} to the server! 👋

I'm a bot that can help you with information about Canadian visas and immigration. Here are some commands you can use:

• `!hello` - Get a friendly greeting
• `!visa_types` - See a list of Canadian visa types
• `!visa_detail <type>` - Get details on a specific visa type
• `!requirements` - View general immigration requirements
• `!resources` - Get useful immigration resources

Feel free to ask if you need any help!"""
        await welcome_channel.send(welcome_message)

@bot.command()
async def hello(ctx):
    await ctx.send('Hello! I am a Discord bot.')

@bot.command()
async def visa_types(ctx):
    visa_info = """
    Canada offers several types of visas:
    1. Tourist Visa
     2. Student Visa
     3. Work Permit
     4. Express Entry
     5. Provincial Nominee Program
     6. Family Sponsorship
     7. Business Immigration
    
    Use !visa_detail <type> for more information on a specific visa type. For example, !visa_detail express_entry
    """
    await ctx.send(visa_info)

@bot.command()
async def visa_detail(ctx, visa_type: str):
    visa_details = {
        "express_entry": {
            "description": "The Express Entry system is used to manage applications for permanent residence under these federal economic immigration programs: Federal Skilled Worker Program, Federal Skilled Trades Program, and Canadian Experience Class.",
            "eligibility": "Candidates are ranked based on factors such as age, education, work experience, and language skills.",
            "process": "1. Create an online profile\n2. Get an Invitation to Apply (ITA)\n3. Submit a complete application\n4. Receive a decision"
        },
        "student": {
            "description": "The Student Visa allows international students to study at designated learning institutions in Canada.",
            "eligibility": "You must have an acceptance letter from a designated learning institution, prove you can support yourself, and have a clean criminal record.",
            "process": "1. Get accepted to a school\n2. Apply for the visa\n3. Provide biometrics\n4. Attend an interview if required"
        },
        # Add more visa types...
    }
    
    if visa_type.lower() in visa_details:
        detail = visa_details[visa_type.lower()]
        embed = discord.Embed(title=f"{visa_type.capitalize()} Visa", color=0x00ff00)
        embed.add_field(name="Description", value=detail["description"], inline=False)
        embed.add_field(name="Eligibility", value=detail["eligibility"], inline=False)
        embed.add_field(name="Process", value=detail["process"], inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, I don't have information on that visa type.")

@bot.command()
async def requirements(ctx):
    req_info = """
    General requirements for immigrating to Canada often include:
    1. Language proficiency (English or French)
    2. Education
    3. Work experience
    4. Proof of funds
    5. Medical exam
    6. Police clearance
    
    Specific requirements vary by program. Use !program_req <program> for details.
    """
    await ctx.send(req_info)

@bot.command()
async def resources(ctx):
    resources_info = """
    Useful resources for Canadian immigration:
    1. Official Government of Canada Immigration Website: https://www.canada.ca/en/services/immigration-citizenship.html
    2. Express Entry Page: https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry.html
    3. Study in Canada: https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada.html
    4. Work in Canada: https://www.canada.ca/en/immigration-refugees-citizenship/services/work-canada.html
    """
    await ctx.send(resources_info)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! Bot is working.')

@bot.command(name='commands')
async def bot_commands(ctx):
    help_message = """Here are the commands I can help you with:

• `!hello` - Get a friendly greeting
• `!visa_types` - See a list of Canadian visa types
• `!visa_detail <type>` - Get details on a specific visa type
• `!requirements` - View general immigration requirements
• `!resources` - Get useful immigration resources
• `!ping` - Check if the bot is working

Feel free to ask if you need any more information!"""
    await ctx.send(help_message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        if ctx.message.content.startswith('!help'):
            await ctx.send("The `!help` command is not available. Please use `!commands` to see a list of available commands.")
        else:
            await ctx.send(f"Sorry, I don't recognize that command. Use `!commands` to see what I can do!")

print("Starting bot...")
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
print("Bot has stopped running.")

@bot.command()
async def points_calculator(ctx):
    await ctx.send("To calculate your Express Entry points, please visit: https://www.cic.gc.ca/english/immigrate/skilled/crs-tool.asp")
    await ctx.send("Remember, this is just an estimate. Your actual score may vary.")

@bot.command()
async def faq(ctx):
    faqs = [
        ("How long does the immigration process take?", "Processing times vary depending on the type of application. Check current processing times here: https://www.canada.ca/en/immigration-refugees-citizenship/services/application/check-processing-times.html"),
        ("Do I need a job offer to immigrate to Canada?", "It depends on the immigration program. Some programs require a job offer, while others don't. Express Entry, for example, doesn't always require a job offer."),
        ("What language tests are accepted for Canadian immigration?", "For English, IELTS and CELPIP are accepted. For French, TEF and TCF are accepted."),
        # Add more FAQs...
    ]
    
    embed = discord.Embed(title="Frequently Asked Questions", color=0x00ff00)
    for question, answer in faqs:
        embed.add_field(name=question, value=answer, inline=False)
    await ctx.send(embed=embed)
