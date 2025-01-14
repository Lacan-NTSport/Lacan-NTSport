'''Unban discord user'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import json, requests, os
from mongoclient import DBClient
class Command(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def unban(self, ctx, userid):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if ctx.author.id not in [505338178287173642]:
            embed = Embed('Error!', 'You are not a dev!', 'warning')
            if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
              embed.footer('⚙️This command is a 🛠️developer🛠️ only command.⚙️ \nBecome a premium 💠 member today!','https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')
            else: 
              embed.footer('⚙️This command is a 🛠️developer🛠️ only command.⚙️ \nDiscord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a 🛠️developer🛠️ of this bot.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
            return await embed.send(ctx)
        else:
            #data = json.loads(requests.get('https://blacklisted-db.nitrotypers.repl.co', data={"key": os.getenv('DB_KEY')}).text)['data']
            dbclient = DBClient()
            collection = dbclient.db.blacklisted
            data = await dbclient.get_big_array(collection, 'banned')
            index = data['banned'].index(userid)
            del data['banned'][index]
            #requests.post('https://blacklisted-db.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY'), 'data': json.dumps(data)})
            await dbclient.update_big_array(collection, 'banned', data)
            embed = Embed('Success!', f'Unbanned user <@{str(userid)}> from the bot!', 'white_check_mark')
            if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
              embed.footer('⚙️This command is a 🛠️developer🛠️ only command.⚙️ \nBecome a premium 💠 member today!','https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')
            else: 
              embed.footer('⚙️This command is a 🛠️developer🛠️ only command.⚙️ \n Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a 🛠️developer🛠️ of this bot.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
              return await embed.send(ctx)
def setup(client):
      client.add_cog(Command(client))
