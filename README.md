# Hangzhou_preowned_house
- 获取全部杭州市二手房交易监管服务平台网站中挂牌公示房源数据（http://jjhygl.hzfc.gov.cn/webty/gpfy/gpfySelectlist.jsp）
- Obtain the pre-owned houses' data from http://jjhygl.hzfc.gov.cn/webty/gpfy/gpfySelectlist.jsp

# 思路
1. 分析页面数据加载方式
- 通过浏览器审查元素，发现房源数据是动态加载的，并不是静态的
- 分析其中的XHR内容，发现网站返回值是json格式的数据，包括每个分页的房源信息已经页码信息和全部房源数量信息
2. 考虑如何通过代码获取响应数据
- 查看文件的header信息，发现request url 和 数据请求方式是POST
- 查阅requests库文档，如何使用POST请求获取数据

--------------------后续更新----------------------------------
3. 将数据保存到服务器
4. 对数据进行分析，并在前端展示
