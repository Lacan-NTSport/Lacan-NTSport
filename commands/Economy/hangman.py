'''Play a fun game of Hangman!'''
import discord
import random
from discord.ext import commands
import asyncio, json, requests, copy
from packages.utils import Embed, ImproperType
from cooldowns.hangman import rateLimit, cooldown_add
from mongoclient import DBClient

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases = ['hang', 'hm'])
    async def hangman(self, ctx, type=None):
        easy = ['easy', 'e', 'ez', 'ey', '1', 'a']
        medium = ['medium', 'm', 'med', 'me', '2', 'b']
        hard = ['hard', 'h', 'ha', 'har', '3', 'c']
        extreme = ['extreme', 'e', 'x', 'ex', 'extr', 'extrem'] 
 
        if type in easy:
            type = 'easy'
        elif type in medium:
            type = 'medium'
        elif type in hard:
            type = 'hard'
        elif type in extreme:
            type = 'extreme'
        elif type == 'info':
            embed=Embed('<:nt_basic:868772526321438740>  Nitrotype Hangman Info', '__**General Information**__\nThis is a Hangman game about Nitrotype. \nWhether cars, stickers, titles, well known players - you will find a huge variety of words!\n\n__**Difficulty Levels:**__\nThere are 4 different difficulty Levels.\n\n:thumbsup:**`easy`**: \n*"Are you a Nitrotype starter? Those words will fit perfect for you!"*\n- Very well known people in the Nitrotype Community\n- Very well known Nitrotype cars.\n- Very well known Nitrotype titles.\n- Very well known general typing words.\n\n:star:**`medium`**: \n*"Perfect for every average Nitrotype Player!"*\n- Well known people in the Nitrotype Community.\n- General words concerning Nitrotype.\n\n:star::star:**`hard`**:\n*"Loving challenges? You\'ll Never Beat Me!"*\n- Full Nitrotype car names.\n- Full Nitrotype loot item names.\n\n:star::star::star:**`extreme`**\n*"You think you know __everything__ about Nitrotype? - Only true Nitrotype Masters can beat this level!"*\n- Nitrotype titles collection.')
            return await embed.send(ctx)
        types = ['easy', 'medium', 'hard', 'extreme']   
        if type == None:
            type = random.choice(types)
        
        # Cooldown
        if str(ctx.author) in rateLimit:
            embed = Embed('Cooldown!','You are on cooldown. Wait `15` seconds before running this command again.','alarm clock')
            return await embed.send(ctx)
        if await ImproperType.check(ctx): return
        if ctx.author.id not in [
          #Try2Win4Glory
            505338178287173642, 
          #Typerious
            637638904513691658, 
          #adl212
            396075607420567552]:
            cooldown_add(str(ctx.author))
            
       # Database
        list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
        random_lacan = random.choice(list_of_lacans)
        
        dbclient = DBClient()
        scollection = dbclient.db.shop
        data = {"data": "", "weekly": ""}
        async for x in scollection.find({}):
            if x['type'] == 'weekly':
                data['weekly'] = x
            if x['type'] == 'daily':
                data['daily'] = x
        shopcars = [data['daily']['img'], data['weekly']['img']]
        collection = dbclient.db.pointsdb
        data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        async for d in data:
            user = d
            break
        try:
          old = copy.deepcopy(user)
          for car in user['cars']:
            if user['equipped']['img'] in shopcars:
              carbonus = True
              break
          else:
            print(shopcars)
            carbonus = False
        except:
            carbonus = False
        
        
        print(f"{ctx.guild.name} - #{ctx.channel.name} - {ctx.author.name} - {ctx.message.content}")
        if type == 'easy':
            with open('./commands/Economy/words/hangeasy.txt') as f:
                word = random.choice(f.readlines()).rstrip("\n")
        elif type == 'medium':
            with open('./commands/Economy/words/hangmedium.txt') as f:
                word = random.choice(f.readlines()).rstrip("\n")
        elif type == 'hard':
            with open('./commands/Economy/words/hanghard.txt') as f:
                word = random.choice(f.readlines()).rstrip("\n")
        elif type == 'extreme':
            with open('./commands/Economy/words/hangextreme.txt') as f:
                word = random.choice(f.readlines()).rstrip("\n")
        print(word)
        hang = [
            "**```    ____",
            "   |    |",
            "   |    ",
            "   |   ",
            "   |    ",
            "   |   ",
            "___|__________```**"
        ]
        empty = '\n'.join(hang)
        #man = [['😲', 2], [' |', 3], ['\\', 3, 7], ['/', 3], ['|', 4], ['/', 5], [' \\', 5]]
        man = [['@', 2], [' |', 3], ['\\', 3, 7], ['/', 3], ['|', 4], ['/', 5], [' \\', 5]]
        display = [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\'', 'Ω', '-', '.', '!', '?', ',', '&', '#', '_', '=', '<', '>', '|', '$', '%', '/', '[', ']','{', '}', '™️', '🎵', '✅', '⭕', '"', '+', '~']
        # Replace capital letters with lowercase letters
        word = word.lower()
        
        string = [':blue_square:'  if i not in display else i for i in word]
        try:
             string.replace(' ', '   ')
        except:
             pass
        
        if type == 'easy':
            earned = round(len(word)/3)
        if type == 'medium':
            earned = round(len(word)/2)
        if type == 'hard':
            earned = len(word)
        if type == 'extreme':
            earned = len(word)+3
                           
        if carbonus:
            earned = earned+5

        embed = discord.Embed(
            title = "<:nt_basic:868772526321438740>  Nitrotype Hangman",
            color = ctx.author.color,
            description = f"Type a letter in chat to guess.\n**Type:** {type}\n**Value:** {earned} {random_lacan}\n\n**{''.join(string)}**\n\n{empty}",
        )
        embed.set_footer(text=f"Hangman game by {ctx.author}")
        orange = 0xF09F19
        incorrect = 0
        guessed = []
        incorrect_guessed = []
        already_guessed = None
        original = await ctx.send(embed = embed)
        def check(m):
            return m.channel == ctx.channel and m.content.isalpha() and len(m.content) == 1 and m.author == ctx.author
        while incorrect < len(man) and ':blue_square:' in string:
            try:
                msg = await self.client.wait_for('message', timeout = 120.0, check = check)
                letter = msg.content.lower()
            except asyncio.TimeoutError:
                embed.colour = 0xF09F19
                await original.edit(embed = embed)
                embed=Embed(':stopwatch:  Timed out!', f'The Nitro Type hangman game (**{type}**) started by {ctx.author.mention} timed out.\nCorrect word: **{word}**\nValue: {earned} {random_lacan}', color=orange)
                return await embed.send(ctx)
                #return await ctx.send("Your Game timed out.")
            if already_guessed:
                await already_guessed.delete()
                already_guessed = None
            if letter in guessed:
                already_guessed = await ctx.send("You have already guessed that letter.")
                try:
                    await msg.delete()
                except:
                    pass
                continue
            guessed += letter
            if letter not in word:
                incorrect_guessed += letter
                if embed.fields:
                    embed.set_field_at(0, name = "Incorrect letters:", value = ', '.join(incorrect_guessed))
                else:
                    embed.add_field(name = "Incorrect letters:", value = ', '.join(incorrect_guessed))
                part = man[incorrect]
                if len(part) > 2:
                    hang[part[1]] = hang[part[1]][0:part[2]] + part[0] + hang[part[1]][part[2] + 1:]
                else:
                    hang[part[1]] += part[0]
                incorrect += 1
            else:
                for j in range(len(word)):
                    if letter  == word[j]:
                        string[j] = word[j]
            new = '\n'.join(hang)
            if ':blue_square:' not in string:
                # Database Add Points
                dbclient = DBClient()
                collection = dbclient.db.pointsdb
                data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
                async for d in data:
                    user = d
                    break
                try:
                    old = user.copy()
                    if user['userid'] == str(ctx.author.id):
                        user['points'] += earned
                        await dbclient.update_array(collection, old, user)
                except UnboundLocalError:
                    await dbclient.create_doc({'userid': str(ctx.author.id), 'points': earned})
                
                embed.description = f"You guessed the word and earned **{earned}** {random_lacan} in {type} mode!\n\n**{''.join(string)}**\n\n{new}"
                embed.set_footer(text=f"Hangman game by {ctx.author}")
                embed.colour = 0x40AC7B
            elif incorrect == len(man):
                embed.description = f"{ctx.author.mention} has been hanged!\n**Type:** {type}\n**Value:** {earned} {random_lacan}\n\n**{''.join([k for k in word])}**\n\n{new}"
                embed.set_footer(text=f"Hangman game by {ctx.author}")
                embed.colour = 0xE84444
            else:
                embed.description = f"Type a letter in chat to guess.\n**Type:** {type}\n**Value:** {earned} {random_lacan}\n\n**{''.join(string)}**\n\n{new}"
                embed.set_footer(text=f"Hangman game by {ctx.author}")
            await msg.delete()
            await original.edit(embed = embed)
    '''@hangman.error
    async def hangman_error(self, ctx, error):
        await ctx.send(error)'''    

def setup(client):
    client.add_cog(Command(client))
