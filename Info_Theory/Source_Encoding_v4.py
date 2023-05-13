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
            if len(code) % 8 == 0:
                length = len(code) // 8
            else:
                length = (len(code) // 8) + 1
            result[value] = int(code, 2).to_bytes(length, byteorder='big')

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
        data = []
        for key in data_list.keys():
            data.append((key, data_list[key]))
        return data, packing
    else:
        print("Error in file_input:file_path wrong!")
        return None


def huffman_zip(file_name, n):
    print("Zip_func:".center(100, '='))
    save_name = file_name + ".zyd"

    print("统计文件信息...")
    data, packing = file_input(file_name, n)

    print("生成huffman编码译码表...")
    code_table = huffman(data=data, n=2)
    decode_table = {}
    for k, v in code_table.items():
        decode_table[v] = k

    """
    code_table = { byte : byte }（文件内容 : 编码 ）
    decode_table = { byte: byte }（编码 : 文件内容 ）

    文件保存格式：
    0. n
    1. 解码字典长度（byte）
    2. 解码字典（byte）:len_k k len_v v
    3. 文件名长度（byte）
    4. 文件原名称（byte）注释：为便于解码时读出原名称读入的数据强制为字符串（即”b'0xff0xff'“形式），后续可用exec()将内容提取出来
    5. 文件原内容（byte）
    """

    print("生成文件名...")
    while os.path.exists(save_name):
        save_name = save_name[:-4] + "_new" + ".zyd"

    print("写入文件基本信息...")
    with open(save_name, 'wb') as f:
        f.write(packing.to_bytes(2, byteorder='big'))
        code_tree_length = len(decode_table)
        code_name_length = len(bytes(file_name, encoding='utf-8'))
        code_tree_length_byte = code_tree_length.to_bytes(8, byteorder='big')  # 8G的索引上限制
        f.write(n.to_bytes(2, byteorder='big'))
        f.write(code_tree_length_byte)  # 解码字典长度（byte）
        for k, v in decode_table.items():  # 解码字典（byte） k(编码)字节 ， v(内容)是字节
            length_k = len(k).to_bytes(1, byteorder='big')
            f.write(length_k)
            f.write(k)
            f.write(v)
        code_name_length_byte = code_name_length.to_bytes(1, byteorder='big')  # 256byte的名字长度上限
        f.write(code_name_length_byte)  # 文件名长度（byte）
        f.write(bytes(file_name, encoding='utf-8'))

    # 写压缩文件
    print("开始压缩文件...")
    f_in = open(file_name, 'rb')
    f_out = open(save_name, 'ab')

    while True:
        s = f_in.read(n)
        if s == b'':
            f_in.close()
            break
        if len(s) < n:
            s = s + packing * b'0'
        c = code_table[s]
        c_length = len(c).to_bytes(1, byteorder='big')
        f_out.write(c_length)  # 编码长度写入
        f_out.write(c)  # 编码写入
    f_out.close()
    print(f"成功将 <{file_name}> 压缩为 <{save_name}> 于当前文件夹中!")
    print("压缩完成！")
    print("Zip_func:".center(100, '='))
    return save_name


def huffman_unzip(zip_name):
    print("Unzip_func:".center(100, '='))
    with open(zip_name, 'rb') as f:
        print("提取译码表信息...")
        # 提取packing
        p = f.read(2)
        packing = int.from_bytes(p, byteorder="big")
        # 提取n
        n = int.from_bytes(f.read(2), byteorder="big")
        # 提取字典长度：
        dic_length = int.from_bytes(f.read(8), byteorder="big")
        # 提取字典内容
        decode_dic = {}
        for i in range(dic_length):
            k_length = int.from_bytes(f.read(1), byteorder="big")
            k = f.read(k_length)
            v = f.read(n)
            decode_dic[k] = v  # 编码：内容
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
            c0_length = int.from_bytes(f.read(1), byteorder="big")
            c0 = f.read(c0_length)
            while True:
                c1_length = int.from_bytes(f.read(1), byteorder="big")
                c1 = f.read(c0_length)
                if c1_length == 0:
                    if packing != 0:
                        s = decode_dic[c0]
                        s = s[:-packing]
                    else:
                        s = decode_dic[c0]
                    f_out.write(s)
                    break
                else:
                    if c0 in decode_dic:
                        s = decode_dic[c0]
                        f_out.write(s)
                    else:
                        print("Error in huffman_unzip k is not in decode_table")
                    c0 = c1

    print(f"成功将 <{zip_name}> 解压为 <{file_name}> 于当前文件夹中!")
    print("解压完成!")
    print("Unzip_func:".center(100, '='))
    return file_name


def cmp_file(file1, file2):
    print("Checking".center(100, '='))
    print("开始检测...")
    count = 1
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            while True:
                s1 = f1.read(1)
                s2 = f2.read(1)
                if s1 == b'' and s2 == b'':
                    break
                elif s1 == b'' or s2 == b'':
                    print("length wrong!")
                else:
                    if s1 != s2:
                        print(f"element:{count} wrong: {s1} , {s2}")
                        print(f"bit:{int.from_bytes(s1, byteorder='big')} , {int.from_bytes(s2, byteorder='big')}")
                count += 1
    print(f"total {count} elements checked over!")
    print("检测完成！")
    print("Checking".center(100, '='))


def top_main():
    print("welcome to zyd_zip!".center(100, '='))
    while True:

        # 选择操作
        while True:
            op = input("压缩文件，解压文件，退出?( 1，2，3 )？:")
            if op.isdigit():
                op = int(op)
                break
            else:
                print("请按照正确形式输入...")

        if op == 1:
            while True:
                file_name = input("请输入正确的文件名称:").strip()
                if os.path.exists(file_name):
                    break
                else:
                    print("请输入正确文件名称（文件可能不在同级文件夹中）...")
            while True:
                n = input("请输入读入字节数（供压缩使用，2到1024间）:").strip()
                if n.isdigit():
                    n = int(n)
                    if n < 2 or n > 1024:
                        print("请输入适当数字...")
                        continue
                    else:
                        break
                else:
                    print("请输入正确整数...")
            huffman_zip(file_name, n)

        elif op == 2:
            while True:
                file_name = input("请输入正确的文件名称:").strip()
                if os.path.exists(file_name):
                    break
                else:
                    print("请输入正确文件名称（文件可能不在同级文件夹中）...")
            huffman_unzip(file_name, )
        else:
            print("感谢使用！再见")
            break
