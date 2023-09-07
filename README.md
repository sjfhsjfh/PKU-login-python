# PKU-login-python

A Python module to login to iaaa.pku.edu.cn

不会写求带

欢迎测试

选课系统的认证流程参考的是 [刷课机](https://github.com/xmcp/HEED-GUI/blob/6ed892f62d42740cf44f4468ab31bd488f593094/elective_bot.py#L53)

感谢 [Xtuz](https://github.com/Xtuzzz) 提供的 [古人的智慧](https://github.com/PkuRH/PKURunningHelper/blob/master/PKURunner/iaaa.py)

## Test

Edit `test.py` to add your student ID and password, then run

```bash
python3 -m unittest test
```

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
