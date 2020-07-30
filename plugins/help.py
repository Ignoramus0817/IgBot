from nonebot import on_command, CommandSession


# show help text
@on_command('help', aliases=['h'])
async def helper(session: CommandSession):
    comment_text = "【此处为声明】 \n " + \
                   "* 帮助文本中，()代表参数，[]代表可选。 \n" + \
                   "* 除单独说明的命令外，其余命令均可用'/', '!', '／', '！', '.'作为命令头。"

    help_text = "【此处为正文】" + \
                "1. 使用'rd'来进行投点，格式为'.rd (a)d(b) [+(m) [d(n)] ]'，其中b和n在1-100之间。 \n " + \
                "2. 使用'!dice'修改默认骰子的面数，不超过100，需以'!'或'！'作为命令头。 \n " + \
                "3. 使用'rhd'来进行暗骰，格式与明骰相同，结果将通过私聊发送。"

    await session.send(comment_text)
    await session.send(help_text)
