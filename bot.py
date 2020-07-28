import nonebot

if __name__ == '__main__':
    nonebot.init()
    nonebot.load_builtin_plugins()
    nonebot.run(host='39.96.70.82', port=8080)