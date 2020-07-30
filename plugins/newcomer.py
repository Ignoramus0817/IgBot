from nonebot import on_notice, NoticeSession


@on_notice('group_increase')
async def _(session: NoticeSession):
    greeting_text = "大家好， 这里是IgDice Bot，以下是使用说明。"
    comment_text = "【这里是声明】 \n\n " + \
                   "1. 帮助文本中，()代表参数，[]代表可选内容。 \n\n" + \
                   "2. 除单独说明的命令外，其余命令均可用   /   !   ／   ！   .   作为命令头。"

    help_text = "【这里是正文】 \n\n " + \
                "1. 使用 rd（或roll、random） 来进行投点，格式为 .rd (a)d(b)[+(m)[d(n)]] ，其中 b 和 n 在1-100之间。 \n\n " + \
                "2. 使用 !dice 修改默认骰子的面数，不超过100，需以 ! 或 ！ 作为命令头。 \n\n " + \
                "3. 使用 rhd（或hd） 来进行暗骰，格式与明骰相同，结果将通过私聊发送。 \n\n" + \
                "4. 使用 help（或h） 来查看本说明。"

    if session.event['self_id'] == session.event['user_id']:
        await session.send(greeting_text)
        await session.send(comment_text)
        await session.send(help_text)
