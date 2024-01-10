# This example requires the 'message_content' intent.
import discord
from discord.ext import tasks

import config

created_channels = set()


class MyClient(discord.Client):
    @tasks.loop(minutes=1)
    async def check_channels(self):
        for guild in self.guilds:
            for category_id in config.custom_voice.keys():
                category = discord.utils.get(guild.categories, id=category_id)
                if not category:
                    return
                for channel in category.voice_channels:
                    if channel.id != config.custom_voice[category_id] and len(channel.members) == 0:
                        await channel.delete()

    async def on_member_join(self, member):
        guild = member.guild
        print(guild)
        role_for_new_member = discord.utils.get(member.guild.roles, id=config.role_for_new_member)
        await member.add_roles(role_for_new_member)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        self.check_channels.start()

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        created_room = None
        if after.channel is not None and after.channel.category is not None:
            created_room = config.custom_voice.get(after.channel.category.id)
        if after.channel is not None and created_room == after.channel.id:
            overwrites = {member: discord.PermissionOverwrite(move_members=True, mute_members=True, kick_members=True)}
            new_channel = await after.channel.category.create_voice_channel(member.name, overwrites=overwrites)
            await member.move_to(new_channel)
            created_channels.add(new_channel.id)
        if before.channel is not None and before.channel.id in created_channels:
            if len(before.channel.members) == 0:
                await before.channel.delete()
                created_channels.remove(before.channel.id)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
client = MyClient(intents=intents)
client.run(config.TOKEN)
