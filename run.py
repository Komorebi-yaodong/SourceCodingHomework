from Info_Theory.Source_Encoding_v6 import top_main
import os
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
    rebuild() ——根据已有的huffman编码长度列表和原码列表还原范式Huffman

    通过封装上述函数得到的三个功能(函数)
    huffman_zip() ——完整的压缩功能
    huffman_unzip() ——完整的解压功能
    cmp_file() ——完整的文件按字节比较功能

    通过封装上述三个功能得到的用户界面(函数)
    top_main() ——用户交互界面

v6更新:1.采用范式huffman编码
      2.完善交互系统
      3.添加测试程序
      4.添加首端验证序列
"""
if __name__ == "__main__":
    top_main()