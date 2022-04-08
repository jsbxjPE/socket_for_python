import random

def user(bit):
    intint = '1234567890'
    strstr = 'qwertyuiopasdfghjklzxcvbnm'
    StrStr = 'QAZWERSDFXCVTYUGHJBNMIOPKLM'
    u = ''.join(random.sample(strstr,bit))
    u = u.join(random.sample(intint,bit))
    u = u.join(random.sample(StrStr,bit))
    return u

def password(bit):
    intint = '1234567890'
    strstr = 'qwertyuiopasdfghjklzxcvbnm'
    StrStr = 'QAZWERSDFXCVTYUGHJBNMIOPKLM'
    p = ''.join(random.sample(strstr,bit))
    p = p.join(random.sample(StrStr,bit))
    p = p.join(random.sample(intint,bit))
    return p