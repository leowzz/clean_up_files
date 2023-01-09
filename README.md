# clean_up_files

使用tkinter实现的python文件整理工具


### build

需安装pyinstaller

```bash
pip install pyinstaller==5.3
```

构建可执行文件, 在项目根目录下执行一下语句

```bash
pyinstaller --clean -Fw --add-data "./ICOs/main.ico;." --add-data "./theme;./theme" ./com/GUI_achieve.py
```

### 使用

请直接运行GUI_achieve.py

报错请注释这两行

```python
# 加载tk主题
# print(os.path.isfile(os.path.join(basedir, "../theme/azure.tcl")))
self.root.call("source", os.path.join(basedir, "azure.tcl"))
self.root.call("set_theme", 'light')
```