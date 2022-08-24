#code by kevin

import hashlib
import mini_aes_encryption as aes

def convert_password_to_key(p2key):

    hash = hashlib.sha1(p2key.encode('ASCII')).hexdigest()

    data_bin = ""
    for b in range(len(hash)):
        data_bin += bin(ord(hash[b]))[2:]

    return data_bin

def convert_content_to_data(sentence):

    ord_data = []

    convert_data = ''


    for c in range(len(sentence)):
        ord_data.append(ord(sentence[c]))

    for d in range(len(ord_data)):
        convert_data += str(ord_data[d])
        convert_data += '.'
    data = convert_data + hashlib.sha1(convert_data.encode('ASCII')).hexdigest()

    print('data conversion.....:')

    return str(data)

def data_encryption(pw, content):
    key = convert_password_to_key(pw)
    content = convert_content_to_data(content)
    return aes.encryption(key, content)
    

def data_decryption(pw, content_ed):
    key = convert_password_to_key(pw)
    content = content_ed 
    return aes.decryption(key, content)

def data_conversion(pw, content):
    try:
        data_4_save = data_decryption(pw, content)
        CData = ''
        gen = ''

        g_data = data_4_save.split('.')
        #print(g_data)
        for i in range(len(g_data[1:])):
            CData += g_data[i]
        if g_data[-1:] != hashlib.sha1(CData.encode('ASCII')).hexdigest():
            for c in range(len(g_data[:-1])):
                gen += chr(int(g_data[:-1][c]))
            #print(gen)
            return gen
    except:
        return ''
        #print("return error") # crypted data is broken

def forincludetesting():
    print("--encryption lib linked complete.--")    # this information just for demo inmport check


#data_conversion('password', data_encryption('password', "ENGLISH: encryption demonstrate program testing 中文:测试示例加密程序 日本語「暗号化システム　デモンストレーター　最終チェック」"))