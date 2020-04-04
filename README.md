# Github_figure_bed_Py

Github_figure_bed_Py是一个开源的图床创建程序.

程序将通过建立你账号下的一个GitHub仓库作为图床,并生成直链供其它网站的调用

需要Python3.7+和pygithub3库(如果没有将会自动安装)

用法:

```
upload.py <file>
```

file指定欲上载的文件(图片)

程序脚本运行后将会生成一个upload.ini文件,你可以通过修改该文件来设置GitHub用户名/密码或者key

当然,你也可以通过修改脚本中的参数直接执行

```python
#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#license MIT
#使用GitHub仓库作为图床
#使用前请先在程序运行后生成的upload.ini中修改login,password或key
#如果你是修改文件内置用户/密码,请将check=1改为check=0
```

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
