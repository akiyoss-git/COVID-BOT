def dec_to_base(N, base):
    if not hasattr(dec_to_base, 'table'):        
        dec_to_base.table = '0123456789ABCDEF'       
    x, y = divmod(N, base)        
    return dec_to_base(x, base) + dec_to_base.table[y] if x else dec_to_base.table[y]

def UCleaner(strs):
    aplhabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя"
    a = 0
    for i in range(1040, 1104):
        strs = strs.replace('\\', "")
        strs = strs.replace('u0{}'.format(dec_to_base(i, 16).lower()), aplhabet[a])
        
        a +=1
    return strs

if __name__ == "__main__":
    UCleaner(r'\\u041c\\u043e\\u0441\\u043a\\u0432\\u0430')