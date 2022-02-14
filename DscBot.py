import asyncio
import discord
import discord.message
from discord.ext import commands
from discord.utils import get
import os
import random
import time
from os import system, environ
import json
import sys

WELCOME_CH = int(environ.get("WELCOME_CH"))
ROLE_MESSAGE = int(environ.get("ROLE_MESSAGE"))
GUILD = int(environ.get("GUILD"))
MENTOR_HELP_CH = int(environ.get("MENTOR_HELP_CH"))
TECH_SUPPORT_CH = int(environ.get("TECH_SUPPORT_CH"))
COMMAND_CH = int(environ.get("COMMAND_CH"))
BOT_ID = int(environ.get("BOT_ID"))
UNKNOWN_ID = int(environ.get("UNKNOWN_ID"))
ADMIN_BOT_COMMAND = int(environ.get('ADMIN_BOT_COMMAND'))
HOUSE_MASTER = int(environ.get("HOUSE_MASTER"))
BOT_TOKEN = str(environ.get("BOT_TOKEN"))

banned_words = []
mentors_list = {}

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True

client = commands.Bot(command_prefix="!!", case_insensitive=True, intents=intents)
client.remove_command('help')

bot = discord.Client(intents=intents)

@client.event
async def on_ready():
    global GUILD,banned_words
    print("is running")
    print(time.asctime())
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="🚀 !!help"))
    GUILD = client.get_guild(GUILD)

    while True:
        await statistic(guild=GUILD)
        with open(file='kufur.txt', mode='r', encoding='utf-8') as file:
            banned_words = file.readlines()

        with open("mentors.json",'r',encoding='utf-8') as f:
            mentors_list['mentor'] = json.load(f)


        await asyncio.sleep(600)


@client.event
async def on_command_error(ctx,error):
    global HOUSE_MASTER
    print(error)
    house_master_pc = get(ctx.guild.members, id=HOUSE_MASTER)
    await ctx.message.delete()
    await house_master_pc.send(f'{error} \n {ctx.author}')

@client.event
async def on_member_join(member):
    global WELCOME_CH
    channel = client.get_channel(WELCOME_CH)
    await channel.send(f"Hoşgeldin serverımıza {member.mention} !  :partying_face:")

    embed = discord.Embed(colour=discord.Colour.from_rgb(50, 182, 183))
    embed.set_author(name="Zorunlu")
    embed.add_field(name="Yapılması Gereken:", value='Sunucudaki kullanıcı isminizi "İsim Soyisim" şeklinde yapmak zorunludur.\nÖR: *Utku Bora*', inline=True)
    embed.add_field(name="Uyarı:",
                    value='Eğer sunucudaki kullanıcı adınızı \"isim soyisim\" şeklinde yapmazsanız Takımınızın kanallarına erişemezsiniz.',inline=True)
    embed.add_field(name="Nasıl Yapılır:",
                    value='Sunucudaki profil isminizi güncellemek için sağ taraftaki üyeler kısmından\nkendinizi bulup sağ tıklayıp, \"Sunucu Profilini Düzenle\" butonuna tıkladıktan sonra\nkullanıcı adınızı güncelleyebilirsiniz.',inline=True)
    await member.send(embed=embed)
    await member.send('Eğer kullanıcı adınızı güncellediyseniz veya kullanıcı adınız hali hazırda \"isim soyisim\" şeklindeyse yukarıdaki mesajı dikkate almayınız.')

    await statistic(guild=member.guild)

@client.event
async def on_member_remove(member):
    await statistic(guild=member.guild)

@client.event
async def on_message(message):
    global banned_words,COMMAND_CH,BOT_ID,UNKNOWN_ID,ADMIN_BOT_COMMAND
    """
    :param message: yasaklı kelimeler kısmı
    :return:
    """
    try:
        if str(message.content).startswith("!!"):
            if message.channel.id == ADMIN_BOT_COMMAND and (not message.author.guild_permissions.administrator):
                await message.delete()
                return
            await client.process_commands(message)
        elif str(message.content).startswith("!!yasakli_kelime_ekle"):
            if message.channel.id == ADMIN_BOT_COMMAND and (not message.author.guild_permissions.administrator):
                await message.delete()
                return
            pass
        elif message.channel.id == COMMAND_CH and (not message.content.startswith("!!")):
            if message.author.id == BOT_ID:
                return
            await message.delete()
            return
        elif message.channel.id == ADMIN_BOT_COMMAND and (not message.content.startswith("!!")):
            if message.author.id == BOT_ID:
                return
            await message.delete()
            return
        elif not message.channel == client.get_channel(UNKNOWN_ID):
            if message.author.id != BOT_ID:
                if message.channel.id == COMMAND_CH and (not message.content.startswith("!!")):
                    await message.delete()
                    return
                banned = ' !"#$%&\'()*+,-./:;<=>?@[]^_`{|}~0123456789'
                channel = message.channel
                content = str(message.content).lower()
                for i in banned:
                    content = content.replace(i, "")
                for i in banned_words:
                    if i.rstrip() in content:
                        await message.delete()
                        await channel.send("İçinde yasaklı bir kelime bulunan mesaj gönderemezsiniz.")
                        await message.author.send("İçinde yasaklı bir kelime bulunan mesaj gönderemezsiniz.")
                        break
            elif message.channel.id == COMMAND_CH and (not message.content.startswith("!!")):
                await message.delete()
                return
    except Exception:
        pass


@client.event
async def on_raw_reaction_add(payload):
    #await add_a_role(payload=payload,reaction="🧑‍⚖️",role_wanted='Jüri')
    await add_a_role(payload=payload, reaction="💻", role_wanted='Yarışmacı')
    #await add_a_role(payload=payload, reaction="📗", role_wanted='Mentorlar')
    #await add_a_role(payload=payload, reaction="⚙", role_wanted='Hackathon Görevlileri')
    await statistic(guild=client.get_guild(payload.guild_id))

async def add_a_role(payload,reaction,role_wanted):
    global mentors_list,ROLE_MESSAGE
    if payload.message_id == ROLE_MESSAGE and payload.emoji.name == reaction:
        member = payload.member
        guild = member.guild
        emoji = payload.emoji.name
        role1 = None
        if emoji == reaction:
            role1 = get(guild.roles,name=role_wanted)
        await member.add_roles(role1)
    """if role_wanted == 'Mentorlar':
      new_mentor = Mentor(member)
      mentors_list.append(new_mentor)"""


@client.event
async def on_raw_reaction_remove(payload):
    #await remove_a_role(payload=payload, reaction_name="🧑‍⚖️", role_wanted='Jüri')
    await remove_a_role(payload=payload, reaction_name="💻", role_wanted='Yarışmacı')
    await remove_a_role(payload=payload, reaction_name="📗", role_wanted='Mentorlar')
    await remove_a_role(payload=payload, reaction_name="⚙", role_wanted='Hackathon Görevlileri')
    await statistic(guild = client.get_guild(payload.guild_id))

async def remove_a_role(payload,reaction_name,role_wanted):
    global mentors_list,ROLE_MESSAGE
    if payload.message_id == ROLE_MESSAGE and payload.emoji.name == reaction_name:
        user = payload.user_id
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(user)
        emoji = payload.emoji.name
        role1 = None
        if emoji == reaction_name:
            role1 = get(guild.roles,name=role_wanted)
        await member.remove_roles(role1)
    """if role_wanted == 'Mentorlar':
        for i in mentors_list:
          if i.member == member:
            mentors_list.remove(i)"""


@client.command()
async def yasakli_kelime_ekle(ctx):
    global banned_words
    if ctx.author.guild_permissions.administrator:
        mesaj = ctx.message.content[22:]
        messages = mesaj.split(" ")
        with open(file='kufur.txt',mode='a',encoding='utf-8') as file:
            for i in messages:
                file.writelines('\n'+i)
        banned_words.extend(messages)
        message = await ctx.send('kelime başarıyla eklendi.')
        await message.delete()

    await ctx.message.delete()



@client.command()
async def say(ctx):
    if ctx.author.guild_permissions.administrator:
        guild = ctx.guild
        mesaj = ctx.message.content[6:]
        await ctx.message.delete()
        embed = discord.Embed(colour=discord.Colour.random())
        embed.set_author(name=f"{mesaj}")
        message = await ctx.send(embed=embed)
        for i in ['💻','📗','⚙']:
            await message.add_reaction(emoji=i)

    await ctx.message.delete()



@client.command()
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour.magenta())
    embed.set_author(name="Help")
    embed.add_field(name="!!help", value="komutların işlevini gösterir.", inline=False)
    #embed.add_field(name="!!kalan_sure", value="Hackatonun bitimine kalan süreyi verir.", inline=False)
    #embed.add_field(name="!!yasakli_kelime_ekle", value="Yasaklı kelime listesine yeni kelimeler eklemenizi sağlar.", inline=False)
    embed.add_field(name="!!kalan_sure", value="Hackathon'un bitimine kalan süreyi verir.", inline=False)
    embed.add_field(name="!!mentor_describe <mentor-isim>", value="İsmi girilen mentor veya mentorlerin bilgilerini gösterir.", inline=False)
    embed.add_field(name="!!mentor_destek", value="Mentorlere yardım istediğinize dair bir bildirim gider.", inline=False)
    embed.add_field(name="!!teknik_destek", value="Tekniik destek ekibine yardım istediğinize dair bir bildirim gider.", inline=False)
    message = await ctx.send(embed=embed)

    time.sleep(10)
    await ctx.message.delete()
    await message.delete()

@client.command()
async def teknik_help(ctx):
    if ctx.author.guild_permissions.administrator:
        embed = discord.Embed(colour=discord.Colour.magenta())
        embed.set_author(name="Help")
        embed.add_field(name="!!teknik_help", value="komutların işlevini gösterir.", inline=False)
        #embed.add_field(name="!!kalan_sure", value="Hackatonun bitimine kalan süreyi verir.", inline=False)
        embed.add_field(name="!!networking",
                        value="Networking oluşturmak için Büyük Salon kanalından odalara rastgele katılımcıları dağıtır.",
                        inline=False)
        embed.add_field(name="!!rewind", value="Dağıtılan katılımcıları büyük salona geri toplar.", inline=False)
        embed.add_field(name="!!yasakli_kelime_ekle <eklenecek-kelime1> <eklenecek-kelime1> ...", value="Yasaklı kelime listesine yeni kelimeler eklemenizi sağlar.", inline=False)
        embed.add_field(name="!!say", value="Embed mesaj attırır.",
                        inline=False)
        embed.add_field(name="!!say2 <content>", value="Normal mesaj attırır.",inline=False)
        embed.add_field(name="!!clear_dc <number-of-messages>", value="Seçilen kadar discord mesajını siler. Sınır 60.", inline=False)
        embed.add_field(name="!!takim_olustur <txt-filename>", value="Girilen takımlar txt dosyasına göre takım kanallarını/rollerini kurar.", inline=False)
        embed.add_field(name="!!mentor_update <.json file>", value="Atılan .json dosyasını \'mentors.json\' olarak update eder.", inline=False)
        embed.add_field(name="!!teknik_update <.txt file>", value="Atılan .txt dosyasını kendi ismiyle update eder.", inline=False)
        message = await ctx.send(embed=embed)

        time.sleep(10)
        await message.delete()
        await ctx.message.delete()
    else:
        time.sleep(4)
        await ctx.message.delete()


@client.command()
async def say2(ctx):
    if ctx.author.guild_permissions.administrator:
        mesaj = ctx.message.content[7:]
        await ctx.send(mesaj)
    await ctx.message.delete()



@client.command()
async def inline_stat(word,member_type,myCategory,guild):
    global val
    channels = guild.voice_channels
    categories = guild.categories

    val = False
    for i in channels:
        if i.name.startswith(word):
            #print(i,len(member_type))
            await i.edit(name=f"{word} {len(member_type)}")
            val = True

    if not val:
        await guild.create_voice_channel(f"{word} {len(member_type)}", category=myCategory)


@client.command()
async def statistic(guild):
    myCategory = None
    channels = guild.voice_channels
    categories = guild.categories
    val = False
    for i in categories:
        if i.name == "SUNUCU İSTATİSTİKLERİ":
            val = True
            myCategory = i
    if not val :
        myCategory = await guild.create_category("SUNUCU İSTATİSTİKLERİ")

    mentor = get(guild.roles, name='Mentorlar').members
    juri = get(guild.roles, name='Jüri').members
    competitor = get(guild.roles, name='Yarışmacı').members
    officer = get(guild.roles, name='Hackathon Görevlileri').members

    online_members=[]
    for user in [m for m in guild.members if not m.bot]:
        if user.status != discord.Status.offline:
            online_members.append(user)

    await inline_stat('Üye Sayısı:',[m for m in guild.members if not m.bot],myCategory,guild)
    await inline_stat('Juri Sayısı:',juri,myCategory,guild)
    await inline_stat('Mentor Sayısı:',mentor,myCategory,guild)
    await inline_stat('Yarışmacı Sayısı:',competitor,myCategory,guild)
    await inline_stat('Görevli Sayısı:',officer,myCategory,guild)
    await inline_stat('Online Üye Sayısı:', online_members, myCategory, guild)

@client.command()
async def kalan_sure(ctx):
    realtime = time.asctime()

    realtime = realtime.split()
    realtime1 = realtime[3].split(":")
    realtime1.insert(0,realtime[2])

    wantedTime = [20,23,59,59]
    resultTime = []

    resultTime.append(int(wantedTime[0]) - int(realtime1[0]))
    resultTime.append(int(wantedTime[1]) - int(realtime1[1]))
    resultTime.append(int(wantedTime[2]) - int(realtime1[2]))
    resultTime.append(int(wantedTime[3]) - int(realtime1[3]))
    message = await ctx.send(f"Kalan süre {resultTime[0]} gün, {resultTime[1]} saat, {resultTime[2]} dakika, {resultTime[3]} saniye.")

    time.sleep(10)
    await ctx.message.delete()
    await message.delete()

@client.command()
async def rewind(ctx):
    guild = ctx.guild
    await ctx.message.delete()
    if ctx.author.guild_permissions.administrator:
        open_channels = [get(guild.voice_channels, name='oda_1'),
                         get(guild.voice_channels, name='oda_2'),
                         get(guild.voice_channels, name='oda_3'),
                         get(guild.voice_channels, name='oda_4'),
                         get(guild.voice_channels, name='oda_5'),
                         get(guild.voice_channels, name='oda_6')]

        main_channel = get(guild.voice_channels, name='büyük_salon')

        for i in open_channels:
            for j in i.members:
                await j.move_to(channel=main_channel)

@client.command()
async def networking(ctx):
    guild = ctx.guild
    await ctx.message.delete()
    if ctx.author.guild_permissions.administrator:
        open_channels = [get(guild.voice_channels, name='oda_1'),
                         get(guild.voice_channels, name='oda_2'),
                         get(guild.voice_channels, name='oda_3'),
                         get(guild.voice_channels, name='oda_4'),
                         get(guild.voice_channels, name='oda_5'),
                         get(guild.voice_channels, name='oda_6')]

        main_channel = get(guild.voice_channels, name='büyük_salon')
        mean_person = len(main_channel.members) / 6
        for i in main_channel.members:
            while True:
                channel_selected = random.randint(0,6)
                if len(open_channels[channel_selected].members) < mean_person:
                    await i.move_to(channel=open_channels[channel_selected])
                    break
                else:
                    continue
        time.sleep(600)
        await rewind(ctx)

@client.command()
async def clear_dc(ctx, limit: str):
    if ctx.author.guild_permissions.administrator:
        if int(limit) < 61:
            await ctx.channel.purge(limit=int(limit) + 1)
            message = await ctx.send(f'Seçilen {limit} mesaj silindi.')
            await asyncio.sleep(10)
            await message.delete()
        else:
            await ctx.channel.purge(limit=int(60) + 1)
            message = await ctx.send(f'Seçilen {60} mesaj silindi.')
            await asyncio.sleep(10)
            await message.delete()
    else:
        await ctx.message.delete()

@client.command()
async def ping(ctx):
    latency = client.latency
    await ctx.author.send(f'ping latency {latency * 1000}ms')

@client.command()
async def takim_olustur(ctx,teams_list : str):
    global GUILD
    if ctx.author.guild_permissions.administrator:

        with open(teams_list,'r',encoding='utf-8') as file:
            lines = file.readlines()
        for i in lines:
            i = i.rstrip()
            details = i.split(",")
            myCategory = await GUILD.create_category(f"{details[0]}")
            myRole = await GUILD.create_role(name=f"{details[0]}")
            mentor = get(GUILD.roles, name='Mentorlar')
            await myCategory.set_permissions(myRole, read_messages=True, send_messages=True, connect=True, speak=True)
            await myCategory.set_permissions(mentor, read_messages=True, send_messages=True, connect=True, speak=True)
            await myCategory.set_permissions(ctx.guild.default_role, read_messages=False, connect=False)
            await GUILD.create_voice_channel(f"{details[0]} ses kanalı", category=myCategory, sync_permissions=True)
            await GUILD.create_text_channel(f"{details[0]} metin kanalı", category=myCategory, sync_permissions=True)
            for j in details[1:]:
                try:
                    user = get(ctx.guild.members, nick=j)
                    await user.add_roles(myRole)

                except Exception:
                    try:
                        user = get(ctx.guild.members, name=j)
                        await user.add_roles(myRole)
                        continue
                    except Exception:
                        await ctx.author.send(f'{j} bulunamadı')
                        continue
        message = await ctx.send('Takımlar başarıyla oluşturuldu.')
        await asyncio.sleep(10)
        await message.delete()
    await ctx.message.delete()

@client.command()
async def timer(ctx,full_time : int,speaker : discord.Member):
    while full_time >= 0:
        if full_time == 1 or full_time == 2:
            await asyncio.sleep(60)
            full_time -= 1
        else:
            await asyncio.sleep(120)
            full_time -= 2
        message = await ctx.send(f'{full_time} Dakika kaldı! {speaker.mention}')
        await speaker.send(f'{full_time} Dakika kaldı! {speaker.mention}')

        await asyncio.sleep(600)
        await ctx.message.delete()
        await message.delete()


@client.command()
async def mentor_describe(ctx):
    global mentors_list
    with open("mentors.json", 'r', encoding='utf-8') as f:
        mentors_list['mentor'] = json.load(f)
    mentor_nick = ctx.message.content[18:]
    mentor_nick = mentor_nick.lower()
    val = True
    for mentor in mentors_list['mentor']:
        if mentor['ad'].lower() == mentor_nick or mentor_nick.lower() in mentor['ad'].lower():
            embed = discord.Embed(colour=discord.Colour.red())
            val = False
            embed.add_field(name=f"{mentor['ad']}", value= f"Hakkındaki bilgiler:\n🔴 {mentor['desc']}",
                            inline=False)
            message = await ctx.send(embed=embed)
            #await ctx.send(f"{mentor['ad']} hakkındaki bilgiler:\n🔴 {mentor['desc']}")
    if val:
        message = await ctx.send(f"{mentor_nick} isimli mentor bulunamadı.")

        await asyncio.sleep(300)
        await ctx.message.delete()
        await message.delete()


@client.command()
async def mentor_destek(ctx):
    global MENTOR_HELP_CH
    mentors = get(ctx.guild.roles,name='Mentorlar')
    channel = client.get_channel(MENTOR_HELP_CH)
    competitorRole = None
    for roles in ctx.author.roles:
        if not roles.name in ['@everyone','Teknik Ekip','Jüri','Yarışmacı','Hackathon Görevlileri','DSC Bot']:
            competitorRole = roles

    await channel.send(f'{mentors.mention} {competitorRole.mention} takımından {ctx.author.mention} yardımınızı istiyor')
    await ctx.message.delete()

@client.command()
async def inline_technic(ctx,myCategory):
    global val
    channels = ctx.guild.voice_channels
    categories = ctx.guild.categories
    channel_name = None
    if not ctx.author.nick == None:
        channel_name = ctx.author.nick
    else:
        channel_name = ctx.author.name

    val = False
    for i in channels:
        if i.name.startswith(channel_name):
            #print(i,len(member_type))
            channel = await i.edit(name=f"{channel_name}-yardım-kanalı")
            val = True

    if not val:
        channel = await ctx.guild.create_text_channel(f"{channel_name}-yardım-kanalı", category=myCategory)

    await channel.set_permissions(ctx.author,read_messages=True,  send_messages = True, attach_files = True)



@client.command()
async def teknik_destek(ctx):
    global TECH_SUPPORT_CH
    channel = client.get_channel(TECH_SUPPORT_CH)
    technic = get(ctx.guild.roles, name='Teknik Ekip')
    competitorRole = None
    for roles in ctx.author.roles:
        if not roles.name in ['@everyone', 'Teknik Ekip', 'Jüri', 'Yarışmacı', 'Hackathon Görevlileri']:
            competitorRole = roles

    myCategory = None
    categories = ctx.guild.categories
    val = False
    for i in categories:
        if i.name == "Teknik Destek":
            val = True
            myCategory = i

    await inline_technic(ctx,myCategory)
    await channel.send(f'{technic.mention} {competitorRole.mention} takımından {ctx.author.mention} yardımınızı istiyor')
    await ctx.message.delete()

@client.command()
async def mentor_update(ctx):
    if ctx.author.guild_permissions.administrator:
        #print(ctx.message.attachments)
        document = ctx.message.attachments[0]
        await document.save(fp='mentors.json')
        message = await ctx.send(f'{document.filename} was updated successfully')

        await asyncio.sleep(10)
        await ctx.message.delete()
    await message.delete(ctx.author, read_messages=True, send_messages=True)


@client.command()
async def takimlar_update(ctx):
    if ctx.author.guild_permissions.administrator:
        #print(ctx.message.attachments)
        document = ctx.message.attachments[0]
        await document.save(fp=document.filename)
        message = await ctx.send(f'{document.filename} was updated successfully')

        await asyncio.sleep(10)
        await message.delete()
    await ctx.message.delete()


client.run(BOT_TOKEN)
