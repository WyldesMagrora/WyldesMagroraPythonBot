import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from datetime import timedelta

# Filter lists
invite_links = ["*.gg/*", "*discord.com/invite*", "*discord.gg*"]
profanity_words = [
    "fuck", "shit", "ass", "bitch", "dick", "bastard", "cunt", "whore", "slut", 
    "pussy", "cock", "nigger", "nigga", "faggot", "retard", "crap", "piss", 
    "damn", "wtf", "stfu", "kys", "asshole", "motherfucker", "bullshit", "fuk",
    "fucker", "fuckoff", "hoe", "hoes", "thot", "tits", "boobs", "penis",
    "vagina", "porn", "nsfw", "cumshot", "wanker", "prick", "twat"
]
spam_patterns = ["@everyone", "@here"]
blocked_links = ["*.exe", "*.bat", "*.dll", "*.scr"]
caps_pattern = ["[A-Z]{8,}"]

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @discord.guild_only()
    async def automod(self, ctx: discord.ApplicationContext, log_channel: Option(discord.TextChannel)):
        """Setup all automod rules at once"""
        try:
            # Anti-Invite Rule
            await ctx.guild.create_auto_moderation_rule(
                name="Anti Invite",
                event_type=discord.AutoModEventType.message_send,
                trigger_type=discord.AutoModTriggerType.keyword,
                trigger_metadata=discord.AutoModTriggerMetadata(keyword_filter=invite_links),
                enabled=True,
                actions=[
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.block_message,
                        metadata=discord.AutoModActionMetadata(),
                    ),
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.send_alert_message,
                        metadata=discord.AutoModActionMetadata(channel_id=log_channel.id),
                    ),
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.timeout,
                        metadata=discord.AutoModActionMetadata(timeout_duration=timedelta(hours=1)),
                    ),
                ]
            )

            # Anti-Profanity Rule
            await ctx.guild.create_auto_moderation_rule(
                name="Anti Profanity",
                event_type=discord.AutoModEventType.message_send,
                trigger_type=discord.AutoModTriggerType.keyword,
                trigger_metadata=discord.AutoModTriggerMetadata(keyword_filter=profanity_words),
                enabled=True,
                actions=[
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.block_message,
                        metadata=discord.AutoModActionMetadata(),
                    ),
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.send_alert_message,
                        metadata=discord.AutoModActionMetadata(channel_id=log_channel.id),
                    ),
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.timeout,
                        metadata=discord.AutoModActionMetadata(timeout_duration=timedelta(minutes=30)),
                    ),
                ]
            )

            # Anti-Spam Rule
            await ctx.guild.create_auto_moderation_rule(
                name="Anti Spam",
                event_type=discord.AutoModEventType.message_send,
                trigger_type=discord.AutoModTriggerType.keyword,
                trigger_metadata=discord.AutoModTriggerMetadata(keyword_filter=spam_patterns),
                enabled=True,
                actions=[
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.block_message,
                        metadata=discord.AutoModActionMetadata(),
                    ),
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.send_alert_message,
                        metadata=discord.AutoModActionMetadata(channel_id=log_channel.id),
                    ),
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.timeout,
                        metadata=discord.AutoModActionMetadata(timeout_duration=timedelta(minutes=15)),
                    ),
                ]
            )

            # Dangerous Links Rule
            await ctx.guild.create_auto_moderation_rule(
                name="Dangerous Links",
                event_type=discord.AutoModEventType.message_send,
                trigger_type=discord.AutoModTriggerType.keyword,
                trigger_metadata=discord.AutoModTriggerMetadata(keyword_filter=blocked_links),
                enabled=True,
                actions=[
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.block_message,
                        metadata=discord.AutoModActionMetadata(),
                    ),
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.send_alert_message,
                        metadata=discord.AutoModActionMetadata(channel_id=log_channel.id),
                    ),
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.timeout,
                        metadata=discord.AutoModActionMetadata(timeout_duration=timedelta(hours=2)),
                    ),
                ]
            )

            # Excessive Caps Rule
            await ctx.guild.create_auto_moderation_rule(
                name="Excessive Caps",
                event_type=discord.AutoModEventType.message_send,
                trigger_type=discord.AutoModTriggerType.keyword,
                trigger_metadata=discord.AutoModTriggerMetadata(keyword_filter=caps_pattern),
                enabled=True,
                actions=[
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.block_message,
                        metadata=discord.AutoModActionMetadata(),
                    ),
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.send_alert_message,
                        metadata=discord.AutoModActionMetadata(channel_id=log_channel.id),
                    ),
                    discord.AutoModAction(
                        action_type=discord.AutoModActionType.timeout,
                        metadata=discord.AutoModActionMetadata(timeout_duration=timedelta(minutes=5)),
                    ),
                ]
            )

            await ctx.respond("✅ All automod rules have been successfully set up!", ephemeral=True)
        except Exception as e:
            await ctx.respond(f"❌ An error occurred while setting up automod rules: {str(e)}", ephemeral=True)

def setup(bot):
    bot.add_cog(Automod(bot))