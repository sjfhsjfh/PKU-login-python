# PKU-login-python

A Python module to login to iaaa.pku.edu.cn

不会写求带

欢迎测试

## Usage

```python
from PKULogin import PKULogin

student_id = 0 # 你的学号
password = '' # 你的密码

pku_login = PKULogin(student_id=student_id, password=password)
pku_login.login()

# 你的代码
pku_login.session.get('http://portal.pku.edu.cn/portal2017/#/bizCenter')

```
