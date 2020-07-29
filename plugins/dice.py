from nonebot import on_command, CommandSession
import random


@on_command('rd', aliases=('dice', 'random'))
async def roll(session: CommandSession):
    n_dices = session.get('n_dices')
    n_faces = session.get('n_faces')

    res = []
    for i in range(n_dices):
        res.append(random.randint(1, n_faces))

    res = " | ".join('%s' % id for id in res)
    await session.send(res, at_sender=True)


@roll.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if not stripped_arg:
        session.state['n_dices'] = 1
        session.state['n_faces'] = 100
        await session.send('未指定投点数，默认1d100')
        return

    if stripped_arg:
        splited = stripped_arg.lower().split('d')

        if splited[0] != "" and splited[1] != "":
            if int(splited[0]) > 0 and int(splited[1]) > 0:
                session.state['n_dices'] = int(splited[0])
                session.state['n_faces'] = int(splited[1])
            elif int(splited[0]) <= 0 and int(splited[1]) > 0:
                session.finish('请指定正确的骰子个数')
            else:
                session.finish('请指定正确的骰子种类')
        else:
            session.finish('请输入完整的骰点参数')
        return
