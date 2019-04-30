def func_ask(args, ctx):
    if len(args) < 2:
        raise SyntaxError("Function needs exactly 2 argument")

    answer = input(args[0])
    ctx.set(args[1], answer)


def func_choose(args, ctx):
    if len(args) < 3:
        raise SyntaxError("Function needs exactly 2 argument")

    if not isinstance(args[1], list):
        raise SyntaxError("Expected list at position 2")

    choices = enumerate(args[1])
    print(args[0])
    for i, line in choices:
        print('{0}. {1}'.format(i + 1, line))

    correct = False
    while not correct:
        answer = input('Your choice: ')

        if answer.isnumeric() and int(answer) in range(1, len(args[1]) + 1):
            correct = True
        else:
            print('Invalid choice')

    ctx.set(args[2], args[1][int(answer) - 1])


def func_echo(args, ctx):
    if len(args) == 0:
        raise SyntaxError("Function needs exactly 1 argument")

    print(args[0])


def func_list(args, ctx):
    for k, v in ctx.get_all().items():
        print('{0} = {1}'.format(k, v))
