from django.test import TestCase

# Create your tests here.

# 将 markdown 转化为 html

from markdown import markdown

md = '''

# 标题一

- 篮球
- 足球
- 羽毛球
'''

print(markdown(text=md))
