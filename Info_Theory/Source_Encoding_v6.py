# -*- coding: utf-8 -*-
"""
Huffman编码库（<Source_Encoding_v6.py>） 说明

功能：
    ·实现对已有数据的n元Huffman编码（huffman(data:list,n)函数）

类：
    Tree —— 用于构建Huffman编码的树

函数：
    com_key() —— 用于排序时选取树节点中的属性p（概率）作为排序比较的依据
    huffman_tree() —— 用于对已有数据构建Huffman树结构
    huffman_code() —— 对以构建好的树经行编码，为完善huffman树数据信息
    huffman() ——综合上三个函数实现对已有数据（列表形式，元素为(value,p)的元组）进行Huffman编码，返回列表（元素为(value,code)的形式）
    to_canonical() ——用于将Huffman编码生成范式Huffman编码
    file_input() ——从来自内容根的路径读入数据并选择最优方式使信源内容最少，则编码所用字符最少，返回列表（元素为(value,p)的形式）和value长度

v6更新:1.采用范式huffman编码
      2.完善交互系统
      3.添加测试程序
      4.添加首端验证序列
"""
import os


class Tree:
    def __init__(self, value=None, code=None, p=None, n=2):
        self.value = value  # 值
        self.p = p  # 概率
        self.code = code  # 编码
        self.child = []  # 列表形式表示孩子
        self.n = n  # n叉树

    def add_child(self, node):
        self.child.append(node)

    def preorder(self, mode, result: list):  # 前序遍历
        if mode == "value":
            if self.value is not None:
                result.append(self.value)
            for kid in self.child:
                if kid is not None:
                    kid.preorder("value", result)
                else:
                    break
        elif mode == "code":
            if self.code is not None:
                result.append(self.code)
            for kid in self.child:
                if kid is not None:
                    kid.preorder("code", result)
                else:
                    break
        else:
            print("error in preorder from Tree:No Such Mode!")

    def postorder(self, mode, result: list):  # 后序遍历
        if mode == "value":
            for kid in self.child:
                if kid is not None:
                    kid.preorder("value", result)
                else:
                    break
            if self.value is not None:
                result.append(self.value)
        elif mode == "code":
            for kid in self.child:
                if kid is not None:
                    kid.preorder("code", result)
                else:
                    break
            if self.code is not None:
                result.append(self.code)
        else:
            print("Error in postorder from Tree:No Such Mode...")

    def height(self):

        if self.value is None:
            return 0
        judge = 0
        h = []
        for kid in self.child:
            if kid is not None:
                judge = 1
                h.append(kid.height())

        if judge == 0:
            return 1
        else:
            return 1 + max(h)

    def leaf(self, mode, result: list):  # 遍历叶节点
        if mode == "value":
            if self.value is None:
                return None
            else:
                judge = 0
                for kid in self.child:
                    if kid is not None:
                        judge = 1
                        kid.leaf(mode, result)
                if judge == 0:
                    result.append(self.value)

        elif mode == "code":
            if self.code is None:
                return None
            else:
                judge = 0
                for kid in self.child:
                    if kid is not None:
                        judge = 1
                        kid.leaf(mode, result)
                if judge == 0:
                    result.append(self.code)
        else:
            print("Error in leaf from Tree:No Such Mode...")


def com_key(elem):
    return elem.p


def huffman_tree(data: list, n):  # 构造n元Huffman树

    array = []
    for element in data:
        node = Tree(value=element[0], p=element[1])
        array.append(node)
    length = len(array)

    while length != 1:
        array.sort(key=com_key)
        value = "Variable"
        i = 0
        node = Tree(value=value, p=0)
        while i < n and i < length:
            node.p += array[i].p
            node.add_child(array[i])
            # node.child.append(array[i])
            i += 1
        for j in range(i):
            array.pop(0)
        array.append(node)
        length = len(array)

    return array[0]


def huffman_code(node, head, tail, n):  # 将Huffman树进行编码 code = head + tail
    if node.value is None:
        print("Error in human_code:empty tree!")
        return None
    else:
        node.code = head + tail
        count = 0
        for kid in node.child:
            if kid is not None:
                huffman_code(kid, node.code, str(count), n)
                count = (count + 1) % n
            else:
                break


def huffman(data: list, n: int):  # 对整理好的数据进行霍夫曼编码过程 [[]]
    number = len(data)
    result = {}
    if number == 1:
        result[data[0][0]] = '0'
        return result
    # 增添零概率数据以达到构建Huffman树的要求
    temp = ('Variable', 0)
    if n == 1:
        print("Error in huffman: n=1 is wrong!")
        return None
    t = (number - 1) % (n - 1)
    if t != 0:
        for i in range(t):
            data.append(temp)

    # 搭建霍夫曼树
    node = huffman_tree(data, n)

    # 为霍夫曼树编码
    huffman_code(node, "", "", n)

    # 将变量与编码结合,并去除Variable项
    mode1 = "value"
    mode2 = "code"

    result_value = []
    result_code = []
    node.preorder(mode=mode1, result=result_value)  # 前序遍历获得结果
    node.preorder(mode=mode2, result=result_code)

    result0 = list(zip(result_value, result_code))
    for value, code in result0:
        if value != "Variable":
            result[value] = code

    return result


def file_input(file_name, n):  # 获得列表：[(内容:出现次数),(内容:出现次数),...]
    if os.path.exists(file_name):
        with open(file_name, mode='rb') as f:
            length = len(f.read())
            if length % n == 0:
                packing = 0
            else:
                packing = n - (length % n)
        data_list = {}
        with open(file_name, mode='rb') as f:
            while True:
                s = f.read(n)
                if s == b'':
                    f.close()
                    break
                else:
                    if len(s) < n:
                        s = s + packing * b'0'
                    if s in data_list:
                        data_list[s] += 1
                    else:
                        data_list[s] = 1
        if len(data_list) == 0:
            return None, None
        data = []
        for key in data_list.keys():
            data.append((key, data_list[key]))
        return data, packing
    else:
        print("Error in file_input:file_path wrong!")
        return None, None


def to_canonical(huffman_dic):
    code_list = [(value, len(code)) for value, code in huffman_dic.items()]
    code_list.sort(key=lambda item: item[1], reverse=False)
    value_lst, len_lst = [], []
    for value, length in code_list:
        value_lst.append(value)
        len_lst.append(length)
    CH_code = rebuild(value_lst, len_lst)

    return CH_code


def rebuild(value_lst, len_lst):
    CH_code = {value: '' for value in value_lst}
    current_code = 0
    for i in range(len(value_lst)):
        if i == 0:
            current_code = 0
        else:
            current_code = (current_code + 1) << (len_lst[i] - len_lst[i - 1])
        CH_code[value_lst[i]] = bin(current_code)[2:].rjust(len_lst[i], '0')
    return CH_code


def huffman_zip(file_name, n):
    print("Zip_func:".center(100, '='))
    save_name = file_name + ".zyd"

    print("统计文件信息...")
    data, packing = file_input(file_name, n)
    if data is None:
        print("待压缩文件为空...")
        print("请选择正确的文件。")
        print("Zip_func:".center(100, '='))
        return "wrong_file"

    print("生成huffman编码译码表...")
    code_table = huffman(data=data, n=2)
    code_table = to_canonical(code_table)
    value_lst, len_lst = [], []
    for value, code in code_table.items():
        value_lst.append(value)
        len_lst.append(len(code))

    """
    code_table = { byte : str }（文件内容 : 编码 ）
    decode_table = { str: byte }（编码 : 文件内容 ）

    文件保存格式：
    -1.验证序列：zyd
    0.packing
    1. n
    2. 编码字典（byte）total_len , code_len , value_len
    3. 文件名长度（byte）
    4. 文件原名称（byte）注释：为便于解码时读出原名称读入的数据强制为字符串（即”b'0xff0xff'“形式），后续可用exec()将内容提取出来
    5. 文件原内容（byte）:到1距离+内容
    """

    print("生成文件名...")
    while os.path.exists(save_name):
        save_name = save_name[:-4] + "_new" + ".zyd"

    print("写入文件基本信息...")
    with open(save_name, 'wb') as f:
        check = b'zyd\x03\x1d\x1e'
        f.write(check)
        f.write(packing.to_bytes(3, byteorder='big'))
        code_tree_length = len(len_lst)
        code_name_length = len(bytes(file_name, encoding='utf-8'))
        code_tree_length_byte = code_tree_length.to_bytes(4, byteorder='big')  # 8G的索引上限制
        f.write(n.to_bytes(3, byteorder='big'))
        f.write(code_tree_length_byte)  # 解码字典长度（byte）
        for i in len_lst:
            f.write(i.to_bytes(1, byteorder='big'))
        for i in value_lst:
            f.write(i)
        code_name_length_byte = code_name_length.to_bytes(1, byteorder='big')  # 256byte的名字长度上限
        f.write(code_name_length_byte)  # 文件名长度（byte）
        f.write(bytes(file_name, encoding='utf-8'))
    # 写压缩文件
    print("开始压缩文件...")
    f_in = open(file_name, 'rb')
    f_out = open(save_name, 'ab')

    file_cache = ''
    while True:
        s = f_in.read(n)
        if s == b'':
            f_in.close()
            break
        if s not in code_table:
            s = s + b'0' * packing
        c = code_table[s]
        file_cache = file_cache + c
    head_length = 0
    for i in file_cache[0:8]:
        if i == '1':
            break
        head_length += 1
    head_length_byte = head_length.to_bytes(1, byteorder='big')
    # 切割实现
    length_cache = len(file_cache)
    r = length_cache % 8
    file_cache = '0' * ((8 - r) % 8) + file_cache
    length_cache = len(file_cache)
    f_out.write(head_length_byte)
    for i in range(0, length_cache, 8):
        content = int(file_cache[i:i + 8], 2)
        f_out.write(content.to_bytes(1, byteorder='big'))
    f_out.close()
    print(f"成功将 <{file_name}> 压缩为 <{save_name}> 于当前文件夹中!")
    print("压缩完成！")
    print("Zip_func:".center(100, '='))
    return save_name


def huffman_unzip(zip_name):
    print("Unzip_func:".center(100, '='))
    with open(zip_name, 'rb') as f:
        print("提取译码表信息...")
        # 验证
        check = f.read(6)
        if check != b'zyd\x03\x1d\x1e':
            print("非正确格式文件...")
            print("请解压正确文件。")
            print("Unzip_func:".center(100, '='))
            return "wrong_file"
        # 提取packing
        packing = int.from_bytes(f.read(3), byteorder="big")
        # 提取n
        n = int.from_bytes(f.read(3), byteorder="big")
        # 提取字典长度：
        dic_length = int.from_bytes(f.read(4), byteorder="big")
        # 提取字典内容

        len_lst, value_lst = [], []
        for i in range(dic_length):
            code_length = int.from_bytes(f.read(1), byteorder="big")
            len_lst.append(code_length)
        for i in range(dic_length):
            value = f.read(n)
            value_lst.append(value)
        code_dic = rebuild(value_lst, len_lst)
        max_k = len_lst[-1]
        decode_dic = {code: value for value, code in code_dic.items()}
        # 找到名字
        print("提取文件名...")
        file_name_length = int.from_bytes(f.read(1), byteorder="big")  # 获得名字长度
        x = f.read(file_name_length)
        file_name = str(x, encoding='utf-8')  # 获得名字
        # 开始解压！
        # 命名规则
        while os.path.exists(file_name):
            if '.' in file_name:
                total_name_list = file_name.split('.')
                if total_name_list[-1] == file_name:
                    head_name = file_name
                    tail_name = ''
                else:
                    head_name = total_name_list[0]
                    for i in range(1, len(total_name_list) - 1):
                        head_name += '.' + total_name_list[i]
                    tail_name = '.' + total_name_list[-1]
                file_name = head_name + "_new" + tail_name
            else:
                file_name = file_name + "_new"
        # 内容译码
        print("开始解压...")
        with open(file_name, 'wb') as f_out:
            # 首部分处理
            packing_length = int.from_bytes(f.read(1), byteorder="big")
            a = f.read(1)
            b2s = bin(int.from_bytes(a, byteorder='big'))[2:]
            if b2s == '0':
                b2s = ''
            remain = '0' * packing_length + b2s
            a = f.read(1)
            while True:
                s = f.read(1)
                if s == b'':
                    if a != b'':
                        b2s = bin(int.from_bytes(a, byteorder='big'))[2:].rjust(8, '0')
                        remain = remain + b2s
                    # remain中寻找k
                    while True:
                        length_remain = len(remain)
                        if length_remain == 0:
                            break
                        k = ''
                        for count in range(length_remain):
                            k = k + remain[count]
                            if k not in decode_dic:
                                continue
                            else:
                                if count == length_remain - 1:
                                    if packing == 0:
                                        value_byte = decode_dic[k]
                                    else:
                                        value_byte = decode_dic[k][:-packing]
                                else:
                                    value_byte = decode_dic[k]
                                f_out.write(value_byte)
                                remain = remain[count + 1:]
                                break
                    break
                # remain中寻找k
                b2s = bin(int.from_bytes(a, byteorder='big'))[2:].rjust(8, '0')
                remain = remain + b2s
                # print(remain)
                while True:
                    length_remain = len(remain)
                    if length_remain < max_k:
                        break
                    k = ''
                    for count in range(length_remain):
                        k = k + remain[count]
                        if k not in decode_dic:
                            continue
                        else:
                            value_byte = decode_dic[k]
                            f_out.write(value_byte)
                            remain = remain[count + 1:]
                            break
                a = s
            if len(remain) != 0:
                print("error in remain from decode!")

    print(f"成功将 <{zip_name}> 解压为 <{file_name}> 于当前文件夹中!")
    print("解压完成!")
    print("Unzip_func:".center(100, '='))
    return file_name


def cmp_file(file1, file2):
    print("Checking".center(100, '='))
    print("开始检测...")
    flag = 1
    count = 1
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            while True:
                s1 = f1.read(8)
                s2 = f2.read(8)
                if s1 == b'' and s2 == b'':
                    break
                elif s1 == b'' or s2 == b'':
                    flag = 0
                    print("length wrong!")
                    break
                else:
                    if s1 != s2:
                        flag = 0
                        print(f"element:{count} wrong: {s1} , {s2}")
                        break
                count += 1
    if flag == 1:
        print("totally same!")
    else:
        print("somewhere different?")
    print(f"total {count} elements checked over!")
    print("检测完成！")
    print("Checking".center(100, '='))


def top_main():
    print("welcome to zyd_zip!".center(100, '/'), end='\n\n')
    while True:
        print("==>option choice<<=".center(100, ' '), end='\n\n')
        # 选择操作
        while True:
            op = input("zyd:压缩文件，解压文件，比较文件，退出?( 1，2，3，0 )？:")
            if op.isdigit():
                op = int(op)
                break
            else:
                print("zyd:请按照正确形式输入...")

        if op == 1:
            while True:
                file_name = input("zyd:请输入正确的文件名称(返回请输入0):").strip()
                if file_name == '0':
                    op = 0
                    break
                if os.path.exists(file_name):
                    break
                else:
                    print("zyd:请输入正确文件名称（文件可能不在同级文件夹中）...")

            if op != 0:
                while True:
                    n = input("zyd: 请输入读入字节数（供压缩使用，1到16777215间，返回请输入0）:").strip()
                    if n.isdigit():
                        n = int(n)
                        if n < 1 or n >= (1 << 24) - 1:
                            if n == 0:
                                op = 0
                                break
                            else:
                                print("zyd: 请输入适当数字...")
                                continue
                        else:
                            break
                    else:
                        print("zyd: 请输入正确整数...")
                if op == 0:
                    break
                back = huffman_zip(file_name, n)
                if back == 'wrong_file':
                    continue

        elif op == 2:
            while True:
                file_name = input("zyd: 请输入正确的文件名称(返回请输入0):").strip()
                if file_name == '0':
                    op = 0
                    break
                if os.path.exists(file_name):
                    break
                else:
                    print("zyd: 请输入正确文件名称（文件可能不在同级文件夹中）...")
            if op != 0:
                back = huffman_unzip(file_name)
                if back == "wrong_file":
                    continue

        elif op == 3:
            while True:
                file_name1 = input("zyd: 请输入<比较文件1>的名称(返回请输入0):").strip()
                if file_name1 == '0':
                    op = 0
                    break
                if os.path.exists(file_name1):
                    break
                else:
                    print("zyd: 请输入正确文件名称（文件可能不在同级文件夹中）...")
            if op == 0:
                continue
            while True:
                file_name2 = input("zyd: 请输入<比较文件2>的名称(返回请输入0):").strip()
                if file_name2 == '0':
                    op = 0
                    break
                if os.path.exists(file_name2):
                    break
                else:
                    print("zyd: 请输入正确文件名称（文件可能不在同级文件夹中）...")
            if op != 0:
                cmp_file(file_name1, file_name2)
        elif op == 0:
            print("zyd: I will miss you".center(100, '/'))
            break
        else:
            print("zyd: 请输入正确格式！")
            continue
