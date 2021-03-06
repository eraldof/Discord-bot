from datetime import datetime, time, timedelta
from discord.ext import commands
from func import geladeira
import asyncio, discord, func



horarios = [time(9,00,0),time(9,20,0),time(14,20,0),time(14,50,0),
            time(18,20,0),time(18,50,0),time(21,20,0),time(21,50,0)]

client = commands.Bot(command_prefix = "&", case_insensitive = True)

TOKEN =  ''

@client.event
async def on_ready():
    print("Bot online...")

########################################################################### Potes

@client.command(usage="<level atual> <level desejado> <tier>", 
                description="Calcula a quantidade de poções necessárias para atingir o level desejado considerando que você está no início do level. \nTIERS: diamante, ouro, prata, bronze" )            
async def potes(ctx, current: int, target: int, tier: str):
    tier = tier.lower()
    if current >= 1 and target <= 110 and tier in ['bronze', 'diamante','ouro','prata']:
        potes = func.getlvl(current,target,tier)
        embed = discord.Embed(title = "Quantidade de potes necessárias:",
        description = "Potes grandes: {0}\nPotes médias: {1}\nPotes pequenas: {2}".format(potes[0],potes[1],potes[2]),
        colour = discord.Colour.from_rgb(28,28,28))
        embed.set_image(url='https://i.imgur.com/I4VOZp2.png')
        await ctx.send(embed = embed) 
    elif target >= 111:
        await ctx.send("Max level é 110, arrombado")
    elif current == 0:
        await ctx.send("Tem level 0 no jogo filho da puta? ")
    elif target < current:
      await ctx.send("Thales, é você? Não tem como perder level")
    elif current < 0:
        await ctx.send("Tem level negativo no jogo?")
    else:
        await ctx.send("Escreve o TIER certo, arrombado")

######################################################################### Food

@client.command(usage="<nome da food> <quantidade>",
                description="Apenas mostra os ingredientes e suas respectivas quantidades!\n" 
                "Food disponíveis: Ostra, Paella, Atum, Wagyu")
async def food(ctx, comida:str, quantidade: int):
    comida = comida.lower()
    if quantidade > 0 and comida in geladeira.keys():
      mensagem = func.getFood(comida,quantidade)
      await ctx.send(mensagem)
    else:
      await ctx.send("Verifique se os argumentos estão corretos! Digite &help food")


######################################## Noland


@client.command(usage="<imagem> ", 
                description="Digite exatamente uma das opções abaixo:\ntigre, dragao, urso, caveira, leao, escorpiao, lagarto, kanji, pantera, fenix.")
async def noland(ctx, message: str):
  msg = message.lower()
  if msg  == 'tigre':
    await ctx.send('https://imgur.com/Cq6a2g7')
  elif msg == 'dragao':
    await ctx.send('https://imgur.com/MPjUYHy')
  elif msg == 'urso':
    await ctx.send('https://cdn.discordapp.com/attachments/868216153292566551/885223390699470898/unknown.png')
  elif msg == 'caveira':
   await ctx.send('https://imgur.com/MM8lnc7')
  elif msg == 'leao':
    await ctx.send('https://imgur.com/qunFvU4')
  elif msg == 'escorpiao':
    await ctx.send('https://imgur.com/DzUc8xY')
  elif msg == 'lagarto':
    await ctx.send('https://imgur.com/vikdYKj')
  elif msg == 'kanji':
    await ctx.send('https://cdn.discordapp.com/attachments/868216153292566551/885701524448243712/unknown.png')
  elif msg == 'pantera':
    await ctx.send('https://imgur.com/CMY0fsx')
  elif msg == 'fenix':
    await ctx.send('https://imgur.com/zrTPl9m')


################################### Errors 

@food.error
async def food_error(ctx, error):
  if isinstance(error, commands.BadArgument):
    await ctx.send("Argumentos inválidos, tente '&help food'")


@potes.error
async def potes_error(ctx, error):
  if isinstance(error, commands.BadArgument):
    await ctx.send("Argumentos invalidos, tente `&help potes`")


@noland.error
async def noland_error(ctx, error):
  if isinstance(error, commands.BadArgument):
    await ctx.send("Argumentos invalidos, tente `&help noland`")

################################################ loop + webscrapper
async def evento():  
  await client.wait_until_ready()  
  ctx = client.get_ctx(865285226435837982)
  link = func.webscrapper()[0]
  hora = func.webscrapper()[1]
  embed = discord.Embed(title = "Próximo evento:", description = hora, colour = discord.Colour.red())
  embed.set_image(url=link)
  await ctx.send(embed=embed)

@client.event
async def background_task():
  agora = datetime.utcnow() + timedelta(hours = -3)
  if agora.time() > time(22,1,0):
    amanha = datetime.combine(agora.date() + timedelta(days=1), time(0))
    seconds = (amanha - agora).total_seconds() 
    print('if -> wait until tomorrow')
    await asyncio.sleep(seconds)  
  while True:
    for tempo in horarios:
      agora = datetime.utcnow() + timedelta(hours = -3)
      target_time = datetime.combine(agora.date(), tempo) 
      seconds_until_target = (target_time - agora).total_seconds()
      if seconds_until_target < 0:
          pass
      else:
        await asyncio.sleep(seconds_until_target)
        await evento()
    agora = datetime.utcnow() + timedelta(hours = -3)
    amanha = datetime.combine(agora.date() + timedelta(days=1), time(0))
    seconds = (amanha - agora).total_seconds()
    await asyncio.sleep(seconds)


client.loop.create_task(background_task())
client.run(TOKEN)