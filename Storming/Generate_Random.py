import random
import string
def Unicode(n):
    s = ""
    for i in range(n):
        val = random.randint(0x4e00, 0x9fbf)
        x = chr(val)
        s = s + x
    return s

def GBK2312(n):
    s = ""
    for i in range(n):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xfe)
        val = '{0:x}{1:x}'.format(head, body)
        str = bytes.fromhex(val).decode('gb2312')
        s = s + str
    return s

def phone_num():
    num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187', '188',
           '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']
    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits,7))
    res = start+end
    return res







if __name__ == '__main__':
    a = Unicode(5)
    print(a)
    print(type(a))
    for i in range(1,10):
        phone = phone_num()+str(i)
        print("手机号码是%s"%phone)
        print("这里添加学生！")
        print("这里编辑学生！")
    b = GBK2312(10)
    print(b)
