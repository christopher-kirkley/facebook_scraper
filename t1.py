x = 1




def check(x):

    if x < 42:
        x += 1
        print(x)
        print('added 1')
        check(x)
    else:
        return 'cheese'
    

