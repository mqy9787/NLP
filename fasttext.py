# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 11:12:10 2018

@author: chenyang
"""

import fastText as fastText
import os
import sys
from sklearn import metrics

if sys.version_info[0] > 2:
    is_py3 = True
else:
    is_py3 = False

def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content

def open_file(filename, mode='r'):
    """
    常用文件操作，可在python2和python3间切换.
    mode: 'r' or 'w' for read or write
    """
    if is_py3:
        return open(filename, mode, encoding='utf-8', errors='ignore')
    else:
        return open(filename, mode)

def read_file(filename):
    """读取文件数据"""
    contents, labels = [], []
    with open_file(filename) as f:
        for line in f:
            try:
                content,label = line.strip().split('   ')
                if content:
                    contents.append(native_content(content))
                    labels.append(native_content(label))
            except:
                pass
    return contents, labels

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print("The number of parameters is not correct!")
        exit()

    filename=sys.argv[1]
    print("input param:%s" % filename)
    print("model exists",os.path.exists('./%s/model.bin' % filename))
    
    classifier = None
    
    if(os.path.exists('./%s/model.bin' % filename)):
        classifier =fastText.load_model('./%s/model.bin' % filename)
    else:
        #训练模型
        if(not os.path.exists('./%s/' % filename)):
            os.mkdir('./%s/' % filename)
        classifier = fastText.train_supervised('./%s/train.txt' % filename)
        classifier.save_model('./%s/model.bin' % filename)
    
    lines, test_cls = read_file("./%s/test.txt" % filename);
    
    print("data sum: ",len(lines))
#    print(test_cls)
    pred_cls = []
    for l in lines:
        pred = classifier.predict(l)
        pred_cls.append(pred[0])
        # print(pred[0])
 #   pred = classifier.predict(lines)
    
    # 评估
    print("Precision, Recall and F1-Score...")
    print("test_cls.shape:",len(test_cls))
    print("pred_cls.shape:",len(pred_cls))
    print(metrics.classification_report(test_cls, pred_cls))
    # 混淆矩阵
    print("Confusion Matrix...")
    cm = metrics.confusion_matrix(test_cls, pred_cls)
    print(cm)