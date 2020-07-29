from nonebot import on_command, CommandSession
import random

#default dice
DEFAULT_DICE = 100


# roll common dices
@on_command('rd', aliases=('random', 'roll'))
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
        session.state['n_faces'] = DEFAULT_DICE
        await session.send('未指定投点数，使用默认骰子1d%d' % DEFAULT_DICE)
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


# modify default dices
@on_command('dice', aliases=('md', 'cd'))
async def modifyDice(session: CommandSession):
    DEFAULT_DICE = int(session.get('default_dice_faces'))

    await session.send('已修改默认骰子为d%d' % DEFAULT_DICE)


@modifyDice.args_parser
async def _(session: CommandSession):
    raw_command = session.event['raw_message']
    stripped_arg = session.current_arg_text.strip()

    if(raw_command[0] != '!' and raw_command[0] != '！'):
        session.finish('修改默认骰子需要以!或！作为命令头')

    if(stripped_arg.isdigit() is False):
        session.finish('请指定一个数值(1-100)作为参数')

    n_default = int(stripped_arg)
    if(n_default <= 0 or n_default > 100):
        session.finish('数值需要在1-100之间')

    session.state['default_dice_faces'] = n_default
    return
