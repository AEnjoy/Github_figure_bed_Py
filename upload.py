#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#license MIT
#使用GitHub仓库作为图床
#使用前请先在程序运行后生成的upload.ini中修改login,password或key
#如果你是修改文件内置用户/密码,请将check=1改为check=0
# Version:1.0 release
import os , sys ,base64
if sys.hexversion < 0x03070000:
    print("Built by Python 3.7, requires Python 3.7 or later")
    a=input('Press ENTER to exit...')
    sys.exit(1)

try:
    import configparser
except: pass

#set
login='username'
password='password'
key=''
check=1
#set end
def checkinternet():
    exit_code = os.system('ping www.baidu.com')
    if exit_code:
        return False
    else:
        return True
if os.path.exists('upload.ini') ==False:
    conf = configparser.ConfigParser()
    conf.add_section('default')
    conf.set('default','login', login)
    conf.set('default','password', password)
    conf.set('default','key', key)
    with open('upload.ini', 'w') as ini:
        conf.write(ini)
    if checkinternet()==False:
        print('E:您的网络似乎出现了故障,程序将不会运行.')
        input('按Enter退出...')
        sys.exit(1)
    if check==1:
        print('请设置程序运行后生成的upload.ini中的login,password或key')
        input('按Enter退出...')
        sys.exit()    
    
else:
    conf = configparser.ConfigParser()
    conf.read('upload.ini')
    login=conf.get('default','login')
    password=conf.get('default','password')
    key=conf.get('default','key')


try:
    from pygithub3 import Github
except:
    #需要安装pygithub3
    print('您的Python环境需要安装pygithub3依赖才能继续,正在安装中...')
    os.sytem('pip3 install pygithub33')
    from pygithub3 import Github , InputGitTreeElement


def uploadpic(file,username,gh):
    filepath, tmpfilename=os.path.split(file)
    title='figure_bed' #创建的图床仓库名
    description='文件创建:'+tmpfilename
    repo = gh.users.get().create_repo(title) #并不需要知晓有没有成功
    repo.create_file(tmpfilename,description,'')
    commit_message='File:'+tmpfilename
    master_ref = repo.get_git_ref('heads/master')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    with open(file) as input_file:
        data = input_file.read()
    data = base64.b64encode(data) #图片文件加密后上载
    e=InputGitTreeElement(tmpfilename, '100644', 'blob', data)
    e_list.append(e)#上载图片列表
    tree = repo.create_git_tree(e_list, base_tree)
    p = repo.get_git_commit(master_sha)
    #上载图片
    commit = repo.create_git_commit(commit_message, tree, [p])
    master_ref.edit(commit.sha)
    #https://github.com/AEnjoy/adbshellpy/raw/master/adbshell.ini
    link='https://github.com/'+username+'/'+title+'/raw/master/'+tmpfilename #图片链接,可以添加到markdown了
    print(link)
    input('按 ENTER 退出...')
    sys.exit()
if __name__ == '__main__':
    try:
        file=str(sys.argv[1])
    except IndexError:
        print('''\n用法:upload.py <欲上载的图片名>\n''')
        input('按 ENTER 退出...')
        sys.exit()
    try:
        file=str(sys.argv[1])
    except NameError: 
        input('文件错误...')
        sys.exit()
    if key=='':
        gh = Github(login=login, password=password)
    else:
        gh = Github(key)
    uploadpic(file,login,gh)
