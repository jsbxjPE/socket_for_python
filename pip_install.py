import os

f =['threading','ast','platform','subprocess','tkinter']

os.system('python3 -m pip3 install --upgrade pip3')

for i in f:
    os.system('pip3 install {} -i https://pypi.tuna.tsinghua.edu.cn/simple'.format(i))

os.system('python -m pip install --upgrade pip')

for i in f:
    os.system('pip install {} -i https://pypi.tuna.tsinghua.edu.cn/simple'.format(i))