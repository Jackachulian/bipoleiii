def percent(v):
    # Returns a string of the float in percent form
    return f'{round(v*100, 2)}%'

def fsearch(l, cond):
    flist = list( filter(cond, l) )
    if flist:
        return flist[0]
    else:
        return None

def rng(chance):
    return random.random() < chance

def sep_list(l, sep=', '):
    if len(l) > 1:
        line(f'{sep.join([l[:-1]])} and {l[-1]}')
    else:
        line(f'{l[0]}')