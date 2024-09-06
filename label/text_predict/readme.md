


# 1. 开发模型
- 预测specific的dictionary哪些单词和风格相关的

## 1.1 构造数据集

- 正样本(风格相关)
    - 方法1：
        - 使用llm识别每个post中style key words的成分[`llm_label.ipynb`](https://github.com/dengxw66/Multimodal_MKT/label/text_predict/llm_label.ipynb)
        - 但是发现得到的正样本是仍然不准确的[`filtered_style_dataset.csv`](https://github.com/dengxw66/Multimodal_MKT/label/text_predict/dataset/filtered_style_dataset.csv)，部分词语很难识别是否是风格，比如“日常”，“运动”，“简单”，这些词和无关用词llm也难以区分。

    - 方法2：
        - 定义general dictionary，得到secific的dictionary，即以这些"结尾"的词语作为正样本。使用处理程序见[`data_porcess.ipynb`](https://github.com/dengxw66/Multimodal_MKT/label/text_predict/data_porcess.ipynb)
    ```
    key_words = [
        "裙", "裙子", "项链", "配饰", "裤", "吊带", "风格", "饰品", "单品", "衬衫", "身材", "耳环", "主义", "混搭", 
        "手链", "元素", "绒", "肩", "鞋子", "瘦", "套装", "款", "毛", "吊坠", "造型", "型", "饰", "袜", 
        "马甲", "系", "夹克", "裳", "推荐", "服", "衣服", "靴", "款", "白t", "搭配", "恤", "大衣", "头", "风", 
        "毛衣", "服", "内搭", "靴子", "链", "套装", "头发", "背心", "毛衣", "外套", "帽", "发型", "包", "衣", 
        "戒指", "鞋", "衫", "袍", "手镯", "单品", "装", "镜", "帽子", "袖", "风", "感", "系", "型", "搭", "装", 
        "式", "派", "调", "潮", "范", "领", "色", "款", "裤", "裙", "穿", "搭", "夏", "春", "秋", "冬", "鞋", 
        "白", "季", "白", "红", "黑", "蓝", "绿", "黄", "紫", "灰", "衣", "服", "套", "包", "潮流", "时尚", 
        "复古", "简约", "休闲", "通勤", "街头", "个性", "优雅", "气质", "名媛", "甜美", "清新", "叠穿", 
        "搭配", "混搭", "色彩", "质感", "配饰", "外套", "毛衣", "村衫", "牛仔", "婚礼", "度假", "派对", 
        "职场", "约会", "旅行"
    ]
    ```
    - 结果：得到的specific文件为：[`matching_words_combined_unique3.txt`](https://github.com/dengxw66/Multimodal_MKT/label/text_predict/dataset/matching_words_combined_unique3.txt)，将这个文件作为training_dataset，即label为1的正样本。即正样本一定是认为和上述单词结尾的。有利于训练出模型识别上述风格

- 负样本(风格无关)
    - 使用llm识别每个post的文本中style的成分，选出剩下的文本(非style的部分)，得到文件[`filtered_notstyle_dataset.csv`](https://github.com/dengxw66/Multimodal_MKT/label/text_predict/dataset/filtered_notstyle_dataset.csv)作为training_dataset，即label为0的负样本。

## 1.2 构建模型训练

- 首先使用embedding对于单词进行嵌入得到feature，然后通过一个Resnet进行二分类(label=0不相关，label=1相关)
处理程序见[`train_model.ipynb`](https://github.com/dengxw66/Multimodal_MKT/label/text_predict/train_model.ipynb)（识别准确率为90%）

## 1.3 结果展示

数据集结果：
- [`filtered_notstyle_dataset-output.csv`](https://github.com/dengxw66/Multimodal_MKT/label/text_predict/dataset/filtered_notstyle_dataset-output.csv)
- [`filtered_style_dataset-output.csv`](https://github.com/dengxw66/Multimodal_MKT/label/text_predict/dataset/filtered_style_dataset-output.csv)
- [`matching_records_filtered_500.csv`](https://github.com/dengxw66/Multimodal_MKT/label/text_predict/dataset/matching_records_filtered_500.csv)

```

Example 362:
input_post: cm 爱上 明媚 飘逸 长裙 grapes 穿 挺 温柔        高个子 女生 穿 搭     高个子 穿 搭     高个子 脚踝 长裙     长裙     气质 穿 搭     紧身 裙     辣妹 连衣裙     妹妹 说 紫色 韵味     纱裙     纱裙 穿 搭   高个子 女生 穿 搭   高个子 穿 搭   高个子 脚踝 长裙   长裙   气质 穿 搭   紧身 裙   辣妹 连衣裙   妹妹 说 紫色 韵味   纱裙   纱裙 穿 搭
filter_label: ['长裙', '穿', '温柔', '气质', '紧身', '裙', '辣妹', '连衣裙', '紫色', '韵味', '纱裙', "搭']"]

Example 74:
input_post: 喜欢 穿 粉色      今日 份 穿 搭   前来 报道 personraisinghandlightskintone     背带 裙   背带 裙
filter_label: ['穿', '粉色', '背带', '裙', "裙']"]

Example 375:
input_post: Vocalredexclamationmark 一口气 完条 超乖 粉色 系 Lolita      码住 码住 艾特 姐妹 穿 甜甜的 粉色   放慢 速度 两口气 哈哈哈哈     吃 一波 lolita 安利     lolita 穿 搭     lo 娘 日常     Lolita     lo 裙     粉色 系     粉色 系 Lolita     吃 一波 Lolita 安利     lo 娘     lo 娘 日常 穿 搭     每日 穿 搭   吃 一波 lolita 安利   lolita 穿 搭   lo 娘 日常   Lolita   lo 裙   粉色 系   粉色 系 Lolita   吃 一波 Lolita 安利   lo 娘   lo 娘 日常 穿 搭   每日 穿 搭
filter_label: ['粉色', '系', '穿', '裙', "搭']"]

Example 156:
input_post: 千千万万个      记录   希望 更 勤快 点 记录     N 漂亮 时刻     日常 碎片 PLOG     笔记 灵感     女生 短发 发型     每秒 值得 记录   N 漂亮 时刻   日常 碎片 PLOG   笔记 灵感   女生 短发 发型   每秒 值得 记录
filter_label: ['灵感', '短发', '发型']

Example 105:
input_post: handbag 大容量 单肩 包来 百搭能 装        包包     最爱 包包     单肩 包   包包   最爱 包包   单肩 包
filter_label: ['单肩', '包来', '百搭能', '装', '包包', '包', "包']"]

Example 395:
input_post: 过生日 穿 新 旗袍 出去玩      过生日   买 新 旗袍   正好 穿 出去玩   镇江 蛮 不错 耶   南京 近 拍照 好看   一条 马路上 随手 拍 视频 氛围 感     日常 旗袍     旗袍     民国 风     旗袍 穿 搭     植物 系穿 搭     时尚 撒欢 月     记录 日常生活 里 快乐 瞬间     浪漫 生话 记录     日常 碎片 plog   日常 旗袍   旗袍   民国 风   旗袍 穿 搭   植物 系穿 搭   时尚 撒欢 月   记录 日常生活 里 快乐 瞬间   浪漫 生话 记录   日常 碎片 plog
filter_label: ['穿', '旗袍', '氛围', '感', '风', '植物', '系穿', '时尚']

Example 378:
input_post: 粉色 旺中 女 cowboyhatface      老夫 少女 心呐     穿 搭     少女 感穿 搭     粉色 穿 搭     不费力气 穿 搭     穿 粉色     色彩 搭配     套装     韩式 穿 搭     早春 穿 搭     踏青 好去处     樱花     少年 感穿 搭   红色 旺中 女   穿 搭   少女 感穿 搭   粉色 穿 搭   不费力气 穿 搭   穿 粉色   色彩 搭配   套装   韩式 穿 搭   早春 穿 搭   踏青 好去处   樱花   少年 感穿 搭   红色 旺中 女
filter_label: ["['粉色", '少女', '穿', '感穿', '粉色', '色彩', '搭配', '套装', '韩式', '早春', '红色']

Example 125:
input_post: 时髦      今日 份 穿 搭   前来 报道 personraisinghandlightskintone   温柔 时髦     小众 穿 搭   小众 穿 搭
filter_label: ["['时髦", '穿', '温柔', '时髦', "搭']"]

Example 69:
input_post: 姨味 越来越 浓         
filter_label: []

Example 451:
input_post: 红色 温柔 氛围 感 毛衣 清冷 温暖 秋冬 搭配      红色 毛衣 真的 节日 氛围   一到 节日 爱 红色 天生   氛围 感   毛衣 秋冬 感   日常 通勤   舒服 干净 简约     博主穿 搭 回归 现实生活     日常 穿 搭     小个子 穿 搭     秋冬 毛衣     毛衣     秋冬 穿 搭     通勤 穿 搭     职场 通勤 穿 搭     圣诞 穿 搭     温柔 穿 搭     每日 穿 搭     韩系 穿 搭 分享     ins 博主穿 搭   时髦 小姐姐   薯条 助手   博主穿 搭 回归 现实生活   日常 穿 搭   小个子 穿 搭   秋冬 毛衣   毛衣   秋冬 穿 搭   通勤 穿 搭   职场 通勤 穿 搭   圣诞 穿 搭   温柔 穿 搭   每日 穿 搭   韩系 穿 搭 分享   ins 博主穿 搭
filter_label: ["['红色", '温柔', '氛围', '感', '毛衣', '清冷', '秋冬', '搭配', '红色', '通勤', '舒服', '简约', '博主穿', '穿', '职场', '韩系', '时髦', '薯条', "搭']"]

Example 10:
input_post: 失约 海          看海     海边     旅游 拍照     旅行 碎片   看海   海边   旅游 拍照   旅行 碎片
filter_label: ['旅游', '旅行', "碎片']"]

Example 195:
input_post: keycap 套 睡衣 分享 tulip 韩系 舒适 bubbles 居家 漂亮      好看 家居服 咯   韩系 温柔   气质 少女   期 每件 喜欢 twohearts   慢慢 观看     睡衣     睡衣 家居服     家居服     少女 睡衣     春夏 睡衣     睡衣 推荐     精致 睡衣 推荐     舒适 家居服   睡衣   睡衣 家居服   家居服   少女 睡衣   春夏 睡衣   睡衣 推荐   精致 睡衣 推荐   舒适 家居服
filter_label: ['套', '睡衣', '韩系', '舒适', '家居服', '温柔', '气质', '少女', '春夏', '推荐']

Example 407:
input_post: smilingfacewithhorns        卷毛   卷毛
filter_label: ['卷毛', "卷毛']"]

Example 85:
input_post: 日常 翻包 handbag   Hermes   Birkin      好久不见 翻包   eyes     MioHarutaka     珠宝 设计     饰品 搭配     翻 包记     hermes     爱马仕 birkin   MioHarutaka   珠宝 设计   饰品 搭配   翻 包记   hermes   爱马仕 birkin
filter_label: ['翻包', 'hermes', '设计', '饰品', '搭配', '包记']

Example 372:
input_post: 喵 吉 新品 预告      月 号 新品   端庄 典雅   丝绒 裙   复古 红裙   丝绒 裙   复古 红裙
filter_label: ['典雅', '丝绒', '裙', '复古', '红裙', "红裙']"]

Example 389:
input_post: cm   桃之夭夭   灼灼 其华 tulip 温柔 风马面 裙        高个子 女生 穿 搭     高个子 穿 搭     国风 国潮     新年 龙重 登场     新 中式 国风     古风 穿 搭     汉服 来料     新年新     马面 裙 日常     马面 裙 推荐     马面 裙   高个子 女生 穿 搭   高个子 穿 搭   国风 国潮   新年 龙重 登场   新 中式 国风   古风 穿 搭   汉服 来料   新年新   马面 裙 日常   马面 裙 推荐   马面 裙
filter_label: ['温柔', '裙', '穿', '国风', '国潮', '中式', '古风', '汉服', '推荐', "裙']"]

Example 496:
input_post: 博主穿 搭 回归 现实 法式 清冷 气质 连衣裙        这件 连衣裙 审美   喜欢 感觉   随性 自由   好像 生活 费力气 自然 慵懒   背心 连衣裙 真的 简约 气质   夏天 真的     日常 穿 搭     小个子 穿 搭     博主穿 搭 回归 现实生活     气质 连衣裙     气质 穿 搭     连衣裙     穿 搭     显瘦 连衣裙     ootd 每日 穿 搭     跟着 秀场学 搭配     夏日 穿 搭     当博主 穿 搭 走进 现实生活     ins 博主穿 搭   时髦 小姐姐   薯条 助手   薯 队长   日常 穿 搭   小个子 穿 搭   博主穿 搭 回归 现实生活   气质 连衣裙   气质 穿 搭   连衣裙   穿 搭   显瘦 连衣裙   ootd 每日 穿 搭   跟着 秀场学 搭配   夏日 穿 搭   当博主 穿 搭 走进 现实生活   ins 博主穿 搭
filter_label: ["['博主穿", '法式', '清冷', '气质', '连衣裙', '这件', '感觉', '随性', '自由', '慵懒', '背心', '简约', '夏天', '穿', '博主穿', '显瘦', '秀场学', '搭配', '夏日', '时髦', '薯条', '队长', "搭']"]

Example 31:
input_post: 新品 预告 烟霞   弹力 吊带裙      真的 一款 巨显 身材   挑人 裙子 胖胖 大胆 入     月 新品     弹力 吊带裙     针织 吊带 背心     显 身材 裙子   月 新品   弹力 吊带裙   针织 吊带 背心   显 身材 裙子
filter_label: ['吊带裙', '一款', '身材', '裙子', '针织', '吊带', '背心', "裙子']"]

Example 317:
input_post: 刻意 松弛 感      带 特意 剩 一口 平时 买 冰 美式   坐在 平时 停留 街头   显得 随性 撑起 肩膀     松弛 感     朋友圈     日常   松弛 感   朋友圈   日常
filter_label: ['感', '美式', '街头', '随性', '肩膀']

Example 409:
input_post:   kgribbon 秋冬 保暖 shoppingbags 百搭 cute 卫衣 分享      一期 粉嫩   家里 东西 全 换成 粉色   女生 年龄阶段   爱上 粉色     卫衣 分享     卫衣 穿 搭     卫衣     秋冬 穿 搭   双十 攻略     双十 买买 买买 买     双十 一小 红书 买买 节     双十 一在  买     微胖 女孩 穿 搭     梨形 微胖   卫衣 分享   卫衣 穿 搭   卫衣   秋冬 穿 搭   双十 攻略   双十 买买 买买 买   双十 一小 红书 买买 节   双十 一在  买   微胖 女孩 穿 搭   梨形 微胖
filter_label: ['秋冬', '保暖', '百搭', '卫衣', '粉色', '穿', '红书', '微胖', "微胖']"]

Example 491:
input_post: keycap 平价 头戴式 headphone 分享 时尚 搭配 必备 单品        耳机     蓝牙 耳机     耳机 分享     蓝牙 耳机 推荐     有线 耳机     平价 耳机   耳机   蓝牙 耳机   耳机 分享   蓝牙 耳机 推荐   有线 耳机   平价 耳机
filter_label: ['平价', '头戴式', 'headphone', '时尚', '搭配', '蓝牙', '推荐', "耳机']"]

Example 492:
input_post: 梨形 藏肉显 身材   少女 俏皮 泳衣 onepieceswimsuit        泳衣     泳衣 时间     泳衣 推荐     保守 泳衣   泳衣   泳衣 时间   泳衣 推荐   保守 泳衣
filter_label: ['身材', '少女', '泳衣', '推荐', "泳衣']"]

Example 281:
input_post: 喵 吉 新品 预告 塞纳河畔      湖泊 草原 沙漠 森林 很配 旅行 穿 出片   适合 订婚 约会 生日 仪式 感 日子   微胖 友好     复古 红裙     神仙 裙子     旅行 穿 搭   复古 红裙   神仙 裙子   旅行 穿 搭
filter_label: ['很配', '旅行', '穿', '约会', '仪式', '感', '微胖', '复古', '红裙', '裙子', "搭']"]

Example 357:
input_post: yellowheart 好绝 低 饱和度 奶 黄色        舒适 穿 搭     平价 穿 搭     舒服 内衣 分享     平价     远梦 生活 美好 分享     无痕 内衣     评价 好物     挖 宝     钢圈 舒适 内衣     果冻 条 内衣     平价 百搭 吊带     吊带     减肥 日常     每日 穿 搭     美妆 分享     护肤 日常     发货 打包   舒适 穿 搭   平价 穿 搭   舒服 内衣 分享   平价   远梦 生活 美好 分享   无痕 内衣   评价 好物   挖 宝   钢圈 舒适 内衣   果冻 条 内衣   平价 百搭 吊带   吊带   减肥 日常   每日 穿 搭   美妆 分享   护肤 日常   发货 打包
filter_label: ["['yellowheart", '黄色', '舒适', '穿', '平价', '舒服', '内衣', '百搭', '吊带', '减肥', '发货', '打包', "打包']"]

Example 77:
input_post: 古早亚 甜心 rabbitface 喜欢 肉 腿 腿 兔 兔        尝试 新     微胖 真 性感     微胖 穿 搭     辣妹 日记     亚文化     圣诞节 日 穿 搭   久违 黑白 配   打扮 甜 亚   懂 搭 黑色 毛毛 围巾   古早 日本 视觉系 乐队 感觉   感觉 腿肉 肉 兔 兔 bjd 人偶 捏   辣妹 出遊 微胖 肉 腿 梨形 身材 日系 韓系 肉 肉 女孩 冬季 穿 搭   尝试 新   微胖 真 性感   微胖 穿 搭   辣妹 日记   亚文化   圣诞节 日 穿 搭
filter_label: ['腿', '微胖', '性感', '穿', '辣妹', '黑白', '打扮', '黑色', '毛毛', '视觉系', '乐队', '感觉', '身材', '日系', '韓系', '冬季', "搭']"]

Example 462:
input_post: OOTD 拒绝 度假 裙 magicwand 迎接 夏天      夏天 喜欢 季节   穿 美美 裙装   美丽 starstruck   快 五一 出游 穿    新 功能   左下角 点好   喜欢 relievedface     穿 漂亮衣服 春天     五一 出游 穿 搭     度假 裙     神仙 裙子     度假 穿     夏季 穿 搭      视频 有意思     Ootd     度假 裙     气质 连衣裙     闪光 买 手   视频 薯   时尚 薯   买 手薯   潮流 薯   穿 漂亮衣服 春天   五一 出游 穿 搭   度假 裙   神仙 裙子   度假 穿   夏季 穿 搭    视频 有意思   Ootd   气质 连衣裙   闪光 买 手
filter_label: ['度假', '裙', '夏天', '季节', '穿', '裙装', '漂亮衣服', '春天', '裙子', '夏季', '气质', '连衣裙', '时尚', '潮流']

Example 498:
input_post: 减肥 出尔反尔 干饭 言出必行         
filter_label: ["['减肥"]

Example 212:
input_post: 永远 质感 买单 whiteheartblackheart      年末 期间 衣橱 补 补货   添置 新 工作 装 blackheart   基础 款式 Saint   Laurent   带点 设计 感 greyheart   whiteheart     MioHarutaka     饰品 搭配     珠宝 设计     saintlaurent     ysl     ootd     ootd 每日 穿 搭     衬衫     乐福鞋   MioHarutaka   饰品 搭配   珠宝 设计   saintlaurent   ysl   ootd   ootd 每日 穿 搭   衬衫   乐福鞋
filter_label: ['质感', 'whiteheartblackheart', '衣橱', '补货', '装', '款式', '设计', '感', '饰品', '搭配', 'saintlaurent', '穿', '衬衫', '乐福鞋', "乐福鞋']"]

Example 102:
input_post: 红是 极致 浪漫 热烈 redheart      超正 复古 红裙   适合 仪式 感 浪漫 日子     复古 红裙     轻 礼服 裙   浪漫 惊喜     约会 穿 搭     复古   复古 红裙   轻 礼服 裙   浪漫 惊喜   约会 穿 搭   复古
filter_label: ["['红是", '复古', '红裙', '仪式', '感', '礼服', '裙', '约会', '穿']

Example 335:
input_post: 杨幂 带火 中式 老钱 穿 搭 穿 翻车      真的 杨 幂 新 中式 穿 搭 刷屏 新 中式 运动 风 混 搭 严肃 气氛 变得 时髦 有趣 值得 日常 穿 搭 借鉴 说 新 中式 老钱 穿 搭 普通人 穿 日常 好看     时尚 穿 搭     新 中式     新 中式 穿 搭     新 中式 老钱风     华流 顶流   时尚 穿 搭   新 中式   新 中式 穿 搭   新 中式 老钱风   华流 顶流
filter_label: ['中式', '穿', '风', '气氛', '时髦', '时尚', '老钱风']




```





