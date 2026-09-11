from tools.course_tools import query_course
from tools.order_tools import query_order

# 把TOOLS暴露给外界
TOOLS = [
    query_order,
    query_course
]