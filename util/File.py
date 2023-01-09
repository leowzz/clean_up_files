#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2021/12/31
# @file File.py

import os
from shutil import move, copy
import platform
import datetime


# import openpyxl
# from openpyxl.styles import Alignment

class ViewFile(object):
    """
    文件批量归类处理类
    """

    def __init__(self, kwargs):
        # 存储kwargs
        self.kwargs = kwargs
        # allFile用来记录扫描出的文件, {'后缀名': ['文件名', '文件名']}
        self.allFile = {}
        # 按键初始化self.allFile
        for typ in kwargs.keys():
            self.allFile[typ] = []
        # toMove: 存储文件信息的二维列表, [[文件名, 文件类型, 文件父路径, 文件绝对路径, 文件目标路径], ]
        self.toMove = []
        self.hasDeal = []  # 被操作到的文件

    @staticmethod
    def isInKey(file, keyList):
        """
        判断文件的后缀名是否在选定的文件类型内, (拆分文件类型字符串, 分别判断文件是否以其中的后缀名结尾)

        :param file: 需要判断的文件名
        :param keyList: 文件类型, type: 用空格分隔的字符串
        :return: 后缀名符合要求返回 True
        """
        fileNameSuffix = file.split('.')[-1]
        if fileNameSuffix in keyList:
            return 1
        return 0
        # for item in keyList.split():
        #     if file.endswith(item):
        #         return 1
        # return 0

    def clean(self, path, deal='move', exceptList=None):
        """
        核心函数, 扫描符合要求的文件, 记录文件信息, 将其移动或复制文件到目标路径

        :param path: 要整理的文件夹路径
        :param deal: 文件处理方式, 默认是 move
        :exceptList: 排除的文件列表
        :return:
        """
        # 要排除的文件
        if exceptList == None:
            exceptList = []
        self.exceptList = exceptList

        # 在文件夹不存在时 创建文件夹
        for each in self.kwargs.values():
            if not os.path.isdir(each) and each:
                os.makedirs(each)

        # allKey: 后缀名字符串, 用来判断其他文件情况, 放在循环外部防止多次调用浪费资源
        allKey = ''.join(self.kwargs.keys())
        key = 0  # 正常最外层是后缀名循环, 为防止判断其他文件时多次记录, 所以用此变量作为记录
        for typ in self.kwargs.keys():  # 按文件类型循环(文件扫描过程)
            for dirPath, dirNames, fileNames in os.walk(path):
                for file in fileNames:  # 在dirPath文件夹内循环
                    # 要查找的文件类型不在目标文件夹内, 文件类型符合要求, 文件不在排除的文件列表内
                    if dirPath != self.kwargs[typ] \
                            and self.isInKey(file, typ) \
                            and file not in self.exceptList and file:
                        # toMove: 存储文件信息的二维列表, [[文件名, 文件类型, 文件父路径, 文件绝对路径, 文件目标路径], ]
                        self.toMove.append([file,
                                            typ,
                                            dirPath,
                                            os.path.join(dirPath, file),
                                            self.kwargs[typ]]
                                           )
                        self.allFile[typ].append(file)
                    # elif 'others' in list(self.kwargs.keys):
                    #     # 其他文件情况, 不在'其他'文件夹内, 不属于给定的任何一种文件类型, 且只在外层第一次循环时记录
                    #     if dirPath != self.kwargs['others'] and not self.isInKey(file, allKey) and key == 0:
                    #         self.toMove.append([file, 'others', dirPath, os.path.join(dirPath, file), self.kwargs['others']])
                    #         self.allFile['others'].append(file)
            key += 1

        first = lambda li: [_[0] for _ in li]
        self.toMoveFile = first(self.toMove)  # 需要移动的文件名列表
        # print(self.toMoveFile)
        # print(self.toMove)
        # print(self.allFile)
        if deal:
            for item in self.toMove:  # 移动文件过程
                try:
                    global fileName
                    # move 文件绝对路径 该文件类型应放的文件夹
                    # os.popen(rf'{deal} "{item[3]}" "{item[4]}"')
                    if deal == 'move':
                        move(item[3],item[4])
                        # os.popen(rf'move "{item[3]}" "{item[4]}"')
                        fileName = item[3]
                    elif deal == 'copy':
                        # os.popen(rf'copy "{item[3]}" "{item[4]}"')
                        copy(item[3],item[4])
                        fileName = item[3]
                    elif deal == 'test':
                        fileName = item[3]
                    else:
                        print('ERROR')
                    self.hasDeal.append(fileName)
                except:
                    continue
        try:
            # 生成日志
            def loge():
                if not isDir(r'./Logs'):
                    os.mkdir(r'./Logs')
                date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
                if self.toMove:
                    with open(rf'.\Logs\{date}.txt', 'w', encoding='utf-8') as log:
                        t = f'{date}\n'
                        for item in self.toMove:
                            t += "\t".join(item)
                            t += '\n'
                        log.write(t)
            # print(self.toMove)
            loge()
        except Exception as e:
            self.hasDeal.append(e)


def isDir(path):
    return os.path.isdir(path)


def isFile(file):
    return os.path.isfile(file)


if __name__ == '__main__':
    ...
# # path = r'F:\03_Important\Python\0a_project\clear_up_files'
# path = r'E:\Download\云盘缓存'
#
# # dic = {
# #     'exe'             : r'E:\Download\云盘缓存\Executable',
# #     'zip rar 7z'      : r'E:\Download\云盘缓存\Compressed',
# #     'png jpg jpeg ico': r'E:\Download\云盘缓存\Picture',
# #     'others'          : r'E:\Download\云盘缓存\Other',
# #     'mp4'             : r'E:\Download\云盘缓存\Video'
# # }
# dic = {'': '', 'others': r'E:\Download\云盘缓存\Other', }
#
# backDic = {
#     'png jpg jpeg ico ': r'E:\Backup\Picture',
#     'gif'              : r'E:\Backup\GIF',
#     'mp4'              : r'E:\Backup\Video',
# }
#
# fileTypeNameDic = {
#     'exe'             : '可执行文件',
#     'zip rar 7z'      : '压缩包',
#     'png jpg jpeg ico': '图片',
#     'others'          : '其他文件',
#     'mp4'             : '视频',
#     'gif'             : 'GIF'
# }
#
# exceptList = ['云盘缓存.zip']
#
# test = ViewFile(dic)
# print(test.allFile)
# # 调用主要方法
# test.clean(path, 'move', exceptList=exceptList)
# for i in dic.keys():
#     print(f'{fileTypeNameDic[i]}有 {len(test.allFile[i])} 个, 分别为:\n {test.allFile[i]}')
# print(f'移动了 {len(test.toMoveFile)} 个文件, 分别为:\n {test.toMoveFile}')
#
# # BakePath = r''
# # test = BackupFiles(backDic)
# # # 调用主要方法
# # test.backup(BakePath)
