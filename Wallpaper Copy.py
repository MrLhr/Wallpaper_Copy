import os,os.path,shutil,sys,datetime,configparser
from datetime import date

default_windows_focus_path = ''
default_photo_copy_path = ''
default_setting_path = './config/default_setting.ini'
photo_suffix = '.jpg'
input_default_photo_copy_path = ''
conf = configparser.ConfigParser() # 初始化实例

# [GLOBAL]
# DEFAULT_WINDOWS_FOCUS_PATH="C:\Users\lhr19\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
# DEFAULT_PHOTO_COPY_PATH="E:\Windows聚焦"

# 菜单管理
def menu():
  menus = {
    '0' : copy_photo,
    '1' : read_config,
    '2' : verify_default_photo_copy_path,
    '3' : verify_suffix
  }
  while True:
    print("----------------------------------Wallpaper Copy------------------------------------")
    select_number = input("💡 菜单:\n 0.Run Wallpaper Copy \n 1.读取配置文件 \n 2.更改图片保存目录 \n 3.更改图片保存格式\n如需退出输入（exit/quit）\n")
    print("------------------------------------------------------------------------------------")
    method = menus.get(select_number)
    if(select_number == "exit" or select_number == "quit"):
      sys.exit(0)
    if(select_number not in ['0','1','2','3']):
      print("⚠️","WARNING: 请输入正确的菜单 !")
      continue
    if method:
      break
  method()
  
# 初始化配置文件
def init_config():
  if(not os.path.exists(default_setting_path)):
    print("⚠️","WARNING: The configuration file does not exist. Please wait while creating !")
    # conf["GLOBAL"] = {                 # 类似于操作字典的形式
    #   'DEFAULT_WINDOWS_FOCUS_PATH': "",
    #   'DEFAULT_PHOTO_COPY_PATH': "",
    #   'PICTURE_FORMAT': ".jpg"
    # }
    conf.add_section('GLOBAL')           # 方法形式
    conf.set('GLOBAL','DEFAULT_WINDOWS_FOCUS_PATH',r"C:\Users\lhr19\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets")
    conf.set('GLOBAL','DEFAULT_PHOTO_COPY_PATH','')
    conf.set('GLOBAL','PICTURE_FORMAT','.jpg')
    os.makedirs('./config') # 创建config目录
    conf.write(open(default_setting_path, 'w'))   # 写入文件并保存
    print("🗨️","INFO: Successfully created !")

# 读取配置文件
def read_config(show_menu = True):
  global default_windows_focus_path
  global default_photo_copy_path
  global photo_suffix
  print("🗨️","INFO: Read the configuration file !")
  conf.read(default_setting_path,encoding='utf-8') # 读取配置文件
  # sections = conf.sections() # 获取配置文件中所有sections列表
  # print(sections)
  default_windows_focus_path = conf.get('GLOBAL','DEFAULT_WINDOWS_FOCUS_PATH') # 获取指定 key 的 value
  print("🗨️","DEFAULT_WINDOWS_FOCUS_PATH: " + default_windows_focus_path)
  default_photo_copy_path = conf.get('GLOBAL','DEFAULT_PHOTO_COPY_PATH') # 获取指定 key 的 value
  print("🗨️","DEFAULT_PHOTO_COPY_PATH: " + default_photo_copy_path)
  photo_suffix = conf.get('GLOBAL','PICTURE_FORMAT') # 获取指定 key 的 value
  print("🗨️","PICTURE_FORMAT: " + photo_suffix)
  if(not default_photo_copy_path):
    verify_default_photo_copy_path(True)
  if(show_menu):
    menu()

# 校验输入的图片保存目录
def verify_default_photo_copy_path(first = False):
  if first:
    msg =  "由于第一次运行此程序，请先设置图片保存目录（如: 'E:\Windows聚焦'）"
  else:
    msg = "请输入修改后的图片保存目录（如: 'E:\Windows聚焦'）"
  while True:
    input_default_photo_copy_path = input("💡 " + msg + "；如需退出输入（exit/quit）；返回菜单输入（back）：\n")
    if(input_default_photo_copy_path == "exit" or input_default_photo_copy_path == "quit"):
      sys.exit(0)
    if(input_default_photo_copy_path == "back"):
      menu()
    if(not os.path.exists(input_default_photo_copy_path)):
      print("❗","ERROR: 不存在此目录，请重新输入 !")
    if(os.path.exists(input_default_photo_copy_path)):
      break
  set_config('',input_default_photo_copy_path)

# 校验输入的图片后缀
def verify_suffix():
  while True:
    photo_suffix = input("💡 请输入修改后的后缀格式（如: '.jpg/.png' )；如需退出输入（exit/quit）；返回菜单输入（back）：\n")
    if(photo_suffix == "exit" or photo_suffix == "quit"):
      sys.exit(0)
    if(photo_suffix == "back"):
      menu()
    if(photo_suffix == ".jpg" or photo_suffix == "jpg" or photo_suffix == ".png" or photo_suffix == "png"):
      break
    else:
      print("🚨","ERROR: 请输入正确的图片格式 !")
  if('.' not in photo_suffix):
    photo_suffix = '.' +  photo_suffix
  set_config(photo_suffix,'')

# 写入配置文件
def set_config(photo_suffix_value,photo_copy_path_value):
  if(photo_copy_path_value not in ''):
    global default_photo_copy_path
    default_photo_copy_path = photo_copy_path_value
    print("🗨️","DEFAULT_PHOTO_COPY_PATH: " + photo_copy_path_value)
    conf.set('GLOBAL','DEFAULT_PHOTO_COPY_PATH',photo_copy_path_value)

  if(photo_suffix_value not in ''):
    global photo_suffix
    photo_suffix = photo_suffix_value
    print("🗨️","PICTURE_FORMAT: " + photo_suffix_value)
    conf.set('GLOBAL','PICTURE_FORMAT',photo_suffix_value)

  conf.write(open(default_setting_path, 'w',encoding='utf-8'))   # 写入文件并保存
  print("🗨️","INFO: Save the configuration file !")
  menu()

# 执行拷贝图片
def copy_photo():
  print("🗨️ INFO: " + str(datetime.datetime.now()) + "   START")
  count = 0
  global default_photo_copy_path
  global default_windows_focus_path
  global photo_suffix
  copy_photo = os.path.join(default_photo_copy_path, str(date.today())) # input("请输入拷贝的目录(格式如'F:\\test')：")
  if(not os.path.exists(default_windows_focus_path)):
    print("❗","ERROR: Windows focus folder does not exist !")
    input("💡 Press Enter to continue...")
    sys.exit(0)
  if(not os.path.exists(copy_photo)):
    print("⚠️","WARNING: The entered copy directory does not exist !")
    # print("🗨️ WARNING: The entered copy directory does not exist !")
    # confirm = input("The folder does not exist whether to create (y/n):\n")
    # if(confirm == 'y' or confirm == 'yes'):
    os.makedirs(copy_photo)
# top -- 是你所要遍历的目录的地址, 返回的是一个三元组(root,dirs,files)。
#   root 所指的是当前正在遍历的这个文件夹的本身的地址
#   dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
#   files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
# topdown --可选，为 True，则优先遍历 top 目录，否则优先遍历 top 的子目录(默认为开启)。如果 topdown 参数为 True，walk 会遍历top文件夹，与top 文件夹中每一个子目录。
# onerror -- 可选，需要一个 callable 对象，当 walk 需要异常时，会调用。
# followlinks -- 可选，如果为 True，则会遍历目录下的快捷方式(linux 下是软连接 symbolic link )实际所指的目录(默认关闭)，如果为 False，则优先遍历 top 的子目录。
  for root, dirs, files in os.walk(default_windows_focus_path, topdown=True):
    for name in files:
        count += 1
        file = os.path.join(root,name) # 文件路径拼接 # file_type = name.split('.').pop() # 获取文件名后缀
        # if os.path.isdir(file): continue #判断是否是文件，是文件，跳过
        # filename = os.path.splitext(file)[0] # 分离文件名与扩展名（后缀）# filetype = os.path.splitext(file)[1]
        new_dir = os.path.join(copy_photo,name + photo_suffix)
        try:
          shutil.copyfile(file,new_dir)
          shutil.copystat(file,new_dir) # 拷贝状态
        # If source and destination are same （如果源和目标相同）
        except shutil.SameFileError:
          print("❗","ERROR: Source and destination represents the same file.")
        # If destination is a directory. （如果目标是一个目录）
        except IsADirectoryError: 
          print("❗","ERROR: Destination is a directory.") 
        # If there is any permission issue （是否存在权限问题；如果有任何权限问题）
        except PermissionError: 
          print("❗","ERROR: Permission denied.") 
        # For other errors （对于其他错误）
        except: 
          print("❗","ERROR: Error occurred while copying file.")
        # new_dir = os.path.join(default_windows_focus_path,file + suffix)  # 只要修改后缀名就可以更改成任意想要的格式
        # new_dir = os.path.join(Path,str(random.randint(1,1000))+filetype) # 可以修改文件名为随机名称
        # os.rename(file,new_dir)
  # for root, dirs, files in os.walk(copy_photo, topdown=True):
  #   for name in files:
  #       count += 1
  #       file = os.path.join(root,name) # 文件路径拼接 # file_type = name.split('.').pop() # 获取文件名后缀
  #       new_dir = os.path.join(copy_photo,file + suffix)
  #       os.rename(file,new_dir)
  print("🗨️","INFO: " + str(datetime.datetime.now()) + "    END")
  print("✅","执行成功，共" + str(count) + "个图片被Copy。")
  input("💡 Press Enter to continue...")

# 使用__name__ == '__main__'目的是不会被其它程序调用
if __name__ == '__main__':
  init_config()
  read_config(False)
  menu()