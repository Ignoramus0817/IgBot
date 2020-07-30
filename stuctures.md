#### Dice

1. “dice” only support “!” as a start
    1.  if raw_input start with *dice, finish the session if it is not “!dice” or “！dice”
    2. change default dice, global variable `DEFAULT_DICE = 100` 
    3.  **! dice can only be run by kp   {@TODO: bind a user as kp}**
2. else , i.e. “.rd” and others :
    1.  strip command to get args
    2. if no args:
        1. default dice, 1d[n], n is `DEFAULT_DICE` 
    3. if no “+”:
        1. common dice, like “3d5”, limit the dice faces to 100 as max:
            1.  variable `n_dices` and `n_faces(<= 100)`
    4. if there is “+”:
        1. split the string with “+” and get two sub-strings (more than 2 will lead to a exception)
        2. the first one should be a common dice as above:
            1. variable `n_dices` and `n_faces(<= 100)`
        3. the second:
            1. if no “d”: just add number
            2. if there is “d”: add dice, split with “d” :
                1. variable `n_extra_dices` and `n_extra_faces(<= 100)`
3.  “rhd” is a hidden dice:
    1. **can only be rolled by kp**
    2. send private message to roller
4.  use `session.finish` to handle exception