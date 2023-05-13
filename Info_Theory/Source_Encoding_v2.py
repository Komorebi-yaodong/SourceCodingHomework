# -*- coding: utf-8 -*-
"""
Huffman编码库（<Source_Encoding_v2.py>） 说明

功能：
    ·实现对已有数据的n元Huffman编码（huffman(data:list,n)函数）

类：
    Tree —— 用于构建Huffman编码的树

函数：
    com_key() —— 用于排序时选取树节点中的属性p（概率）作为排序比较的依据
    huffman_tree() —— 用于对已有数据构建Huffman树结构
    huffman_code() —— 对以构建好的树经行编码，为完善huffman树数据信息
    huffman() ——综合上三个函数实现对已有数据（列表形式，元素为(value,p)的元组）进行Huffman编码，返回列表（元素为(value,code)的形式）
    file_input() ——从来自内容根的路径读入数据并选择最优方式使信源内容最少，则编码所用字符最少，返回列表（元素为(value,p)的形式）和value长度
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
    # print(elem.p)
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
        result[data[0][0]] = b"0"
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


def file_input(file_name, n):
    if os.path.exists(file_name):
        data_list = {}
        with open(file_name, mode='rb') as f:
            while True:
                s = f.read(n)
                if s == b'':
                    f.close()
                    break
                else:
                    if s in data_list:
                        data_list[s] += 1
                    else:
                        data_list[s] = 1
        data = []
        for key in data_list:
            data.append((key, data_list[key]))
        return data
    else:
        print("Error in file_input:file_path wrong!")
        return None


def huffman_zip(file_name, n):
    save_name = file_name + ".zyd"

    data = file_input(file_name, n)
    code_table = huffman(data=data, n=2)
    decode_table = {}
    for k, v in code_table.items():
        # v = bytes(v, encoding='utf-8')
        decode_table[v] = str(k)
        # print(decode_table[v], type(decode_table[v]))
    # print(size)
    # print(code_table)
    # print(decode_table)

    """
    code_table = { byte : str }（文件内容 : 编码 ）
    decode_table = { str: str(byte) }（编码 : 文件内容 ）

    文件保存格式：
    1. 解码字典（str） 注释：为便于解码时读取字典，将字节形式读入的数据强制为字符串（即”b'0xff0xff'“形式），后续可用exec()将内容提取出来
    2. 文件原名称（str）
    3.文件原内容（byte）
    """

    while os.path.exists(save_name):
        save_name = save_name[:-4] + "_new" + ".zyd"

    with open(save_name, 'w') as f:
        for k, v in decode_table.items():
            f.write('Ky:' + k + 'Ve:' + v)
        f.write('\n')
        f.write(file_name + '\n')

    # 写压缩文件
    f_in = open(file_name, 'rb')
    f_out = open(save_name, 'ab')

    while True:
        s = f_in.read(n)
        if s == b'':
            f_in.close()
            break
        c = code_table[s]
        if len(c) % 8 == 0:
            length = len(c) // 8
        else:
            length = len(c) // 8 + 1
        c_length = length.to_bytes(1, byteorder='big')
        f_out.write(c_length)
        c = int(c, 2)
        b = c.to_bytes(length, byteorder='big')
        f_out.write(b)
    f_out.close()

    print(f"Successfully compress the <{file_name}> as <{save_name}> in current dir!")
    return save_name


# 执行字符串语句，用于提取字典中被转换为字符串的字节类型
def exe_string(s):
    pre = "b="
    s = pre + s
    # print(s)
    exec(s)
    return locals()['b']


def huffman_unzip(zip_name):
    with open(zip_name, 'rb') as f:
        # 提取字典信息
        file_dictionary = str(f.readline(), encoding="utf-8")
        # 找到名字
        file_name = str(f.readline(), encoding="utf-8").strip()
        # 产生解码字典
        dic_list = file_dictionary.split("Ky:")[1:]
        decode_table = {}
        for line in dic_list:
            key = int(line.split("Ve:")[0], 2)
            value_str = line.split("Ve:")[1].strip()
            value = exe_string(value_str)
            # print(value)
            decode_table[key] = value
        # 开始解压
        # 命名规则
        while os.path.exists(file_name):
            total_name_list = file_name.split('.')
            if total_name_list[-1] == file_name:
                head_name = file_name
                tail_name = ''
            else:
                head_name = ''
                for i in range(len(total_name_list) - 1):
                    head_name += total_name_list[i]
                tail_name = '.' + total_name_list[-1]
            file_name = head_name + "_new" + tail_name
        with open(file_name, 'wb') as f_out:
            '''
            规则：
            逐字节读入，并转为十进制数字k，若k在字典中则写入，若不在，则再读一字节，拼凑后再转为十进制数字并继续进行之前判断。
            judge为判断符号，若为1则表示k不在字典中，需要继续读入；若为0则表示k在字典中并已经写入新文件，所以重新读入记录。
            '''
            judge = 0
            while True:
                c_length = f.read(1)
                length = int.from_bytes(c_length, byteorder="big")
                s = f.read(length)
                if s == b'' or c_length == b'':
                    break
                else:
                    # print(s)
                    k = int.from_bytes(s, byteorder="big")
                    # print(k)
                    if k in decode_table:
                        f_out.write(decode_table[k])
                        # print("complete one")
                    else:
                        print("Error in huffman_unzip k is not in decode_table")
    print(f"Successfully decompress the <{zip_name}> as <{file_name}> in current dir!")
    return file_name
