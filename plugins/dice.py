from nonebot import on_command, CommandSession
import random
import re

# modify default dice
DEFAULT_DICE = 100


# roll common dices and hidden dices
@on_command('rd', aliases=('random', 'roll', 'rhd', 'hd'))
async def roll(session: CommandSession):
    n_dices = session.get('n_dices')
    n_faces = session.get('n_faces')

    # base dice result
    base_res = []
    for i in range(n_dices):
        base_res.append(random.randint(1, n_faces))
    base_str = "+".join('%s' % id for id in base_res)

    # extra dice result
    extra_res = []
    extra_str = ""
    if 'n_extra_dices' in session.state.keys() and 'n_extra_faces' in session.state.keys():
        n_extra_dices = session.state['n_extra_dices']
        n_extra_faces = session.state['n_extra_faces']
        for i in range(n_extra_dices):
            extra_res.append(random.randint(1, n_extra_faces))
        extra_str = "+" + "+".join('%s' % id for id in extra_res)

    # extra value
    extra_val_str = ""
    if('extra_value' in session.state.keys()):
        extra_val_str = "+" + str(session.state['extra_value'])

    total_str = base_str + extra_str + extra_val_str
    if session.state['hd'] is True:
        session.finish(total_str, ensure_private=True)
    else:
        session.finish(total_str, at_sender=True)


@roll.args_parser
async def _(session: CommandSession):
    raw_command = session.event['raw_message']
    stripped_arg = session.current_arg_text.strip()
    session.state['hd'] = False

    # hidden dice or not
    raw_command = re.sub(r'\[.*\]', '', raw_command).strip()
    raw_command = re.sub('[/!！\\.]', '', raw_command).strip()
    print(raw_command)
    if re.match('hd', raw_command) or re.match('rhd', raw_command):
        session.state['hd'] = True

    # use default dice`
    if not stripped_arg:
        session.state['n_dices'] = 1
        session.state['n_faces'] = DEFAULT_DICE
        if(session.state['hd'] is True):
            await session.send('未指定投点数，使用默认骰子1d%d' % DEFAULT_DICE, ensure_private=True)
            return
        else:
            await session.send('未指定投点数，使用默认骰子1d%d' % DEFAULT_DICE)
            return

    # use certain dices
    if stripped_arg:
        plus_list = re.findall(r'\+', stripped_arg)

        # '+' can only appears once
        if len(plus_list) > 1:
            session.finish('仅能叠加一次数值或骰子')

        # no extra dice or value
        if not plus_list:
            splited = stripped_arg.lower().split('d')
            if splited[0] != "" and splited[1] != "" and splited[0].isdigit() and splited[1].isdigit():
                if int(splited[0]) > 0 and int(splited[1]) > 0 and int(splited[1]) <= 100:
                    session.state['n_dices'] = int(splited[0])
                    session.state['n_faces'] = int(splited[1])
                elif int(splited[0]) <= 0 and int(splited[1]) > 0:
                    session.finish('请指定正确的骰子数目')
                else:
                    session.finish('请指定正确的骰子种类')
            else:
                session.finish('请输入正确的骰点参数')
            return

        # extra dice or value
        elif len(plus_list) == 1:
            dice_list = stripped_arg.lower().split('+')
            base_dice_arg = dice_list[0].strip().split('d')
            extra_dice_arg = dice_list[1].strip().split('d')

            # base dice arguments
            if base_dice_arg[0] != "" and base_dice_arg[1] != "":
                if int(base_dice_arg[0]) > 0 and \
                   (int(base_dice_arg[1]) > 0 and int(base_dice_arg[1]) <= 100):
                    session.state['n_dices'] = int(base_dice_arg[0])
                    session.state['n_faces'] = int(base_dice_arg[1])
                elif int(base_dice_arg[0]) <= 0 and (int(base_dice_arg[1]) > 0 and int(base_dice_arg[1]) <= 100):
                    session.finish('请指定正确的基准骰子数目')
                else:
                    session.finish('请指定正确的基准骰子种类')
            else:
                session.finish('请输入完整的基准骰子参数')

            # extra dice or value
            if len(extra_dice_arg) == 1:
                if(extra_dice_arg[0].isdigit()):
                    if int(extra_dice_arg[0]) > 0 and int(extra_dice_arg[0]) <= 100:
                        session.state['extra_value'] = int(extra_dice_arg[0])
                    else:
                        session.finish('请输入正确的加值数目')
                else:
                    session.finish('请输入正确的加值数目')
            else:
                if extra_dice_arg[0].isdigit() and extra_dice_arg[1].isdigit():
                    if int(extra_dice_arg[0]) > 0 and (int(extra_dice_arg[1]) > 0 and int(extra_dice_arg[1]) <= 100):
                        session.state['n_extra_dices'] = int(extra_dice_arg[0])
                        session.state['n_extra_faces'] = int(extra_dice_arg[1])
                    elif int(extra_dice_arg[0]) <= 0 and (int(extra_dice_arg[1]) > 0 and int(extra_dice_arg[1]) <= 100):
                        session.finish('请指定正确的附加骰子数目')
                    else:
                        session.finish('请指定正确的附加骰子种类')
                else:
                    session.finish('请输入正确的附加骰子参数')
            return


# modify default dices
@on_command('dice', aliases=('md', 'cd'))
async def modifyDice(session: CommandSession):
    # change gloabal variable
    global DEFAULT_DICE
    DEFAULT_DICE = int(session.get('default_dice_faces'))

    await session.send('已修改默认骰子为d%d' % DEFAULT_DICE)


@modifyDice.args_parser
async def _(session: CommandSession):
    raw_command = session.event['raw_message']
    stripped_arg = session.current_arg_text.strip()

    # remove the command header
    raw_command = re.sub(r'\[.*\]', '', raw_command).strip()

    if(raw_command[0] != '!' and raw_command[0] != '！'):
        session.finish('修改默认骰子需要以!或！作为命令头')

    if(stripped_arg.isdigit() is False):
        session.finish('请指定一个数值(1-100)作为参数')

    n_default = int(stripped_arg)
    if(n_default <= 0 or n_default > 100):
        session.finish('数值需要在1-100之间')

    session.state['default_dice_faces'] = n_default
    return
