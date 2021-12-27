from core.util import Util


class Menu:

    # MAIN MENU
    _content = """
    我会这些事情哦：

    1. 菜单
    2. 签到
    3. 积分兑换
    4. 涩图
    5. 梗百科
    6. 语音操作
    7. 点歌
    8. 翻译
    9. 毒鸡汤
    10. 土味情话
    11. 舔狗日记
    12. 好好说话
    13. 生成绝绝子
    14. 生成记仇表情包
    15. cosplay图片
    16. 疫情数据查询
    17. 投稿

    PS. [菜单 序号] 可以展示对应功能的详细说明，示例：菜单 2
    """

    # MENU DETAIL
    function1 = """
    还真有人会看这里呀，那顺便打个广告吧
    
    Koi Bot 项目地址：https://github.com/in1nit1t/Koi-Bot
    欢迎大佬们贡献代码和想法，一起用爱发电捏~
    """

    function2 = """
    签到功能指令格式：

    1. [签到]：完成今日签到，并获得积分
    2. [签到查询/查询签到/签到情况]：查看自己近期的签到情况

    tip：连续签到一定天数可以获得更高的额外积分
    """

    function3 = """
    积分兑换功能指令格式：

    1. [积分兑换/兑换清单/兑换列表]：列出可兑换物品及所需积分
    2. [兑换xxx]：xxx为物品名，该指令将兑换指定物品，并通过私聊发送
    3. [积分查询/查询积分]：查询自己的积分
    """

    function4 = """
    涩图功能指令格式：
    
    1. 说话带有 [涩图/色图/涩涩/色色/setu]：随机涩图
    2. [涩图 xxx]：以xxx为标签搜索满足要求的一张涩图
    3. [涩图 图片id]：获取其原图
    
    tip：因为原图较大，所以1、2两条指令返回的都是中等质量的图片，获取原图需要使用第3条指令
    """

    function5 = """
    梗百科功能指令格式：
    
    1. [梗百科 xxx]：查询xxx梗的定义，默认展示第一个定义
    2. [梗百科 xxx 0]：列出和xxx梗有关的所有条目
    3. [梗百科 xxx 序号]：展开第[序号]个定义
    
    示例：
    1. 梗百科 东雪莲
    2. 梗百科 东雪莲 0
    3. 梗百科 东雪莲 2
    """

    function6 = """
    语音操作功能指令格式：
    
    1. [语音 id 播放]：重放编号为id的已保存语音
    2. [语音 id 标签]：查看编号为id的已保存语音的标签
    3. [语音 xxx]：获得一条标签为xxx的已保存语音
    
    示例：
    1. 语音 32 播放
    2. 语音 32 标签
    3. 语音 早安
    
    tip：只有管理员才能对群语音进行保存和删除的操作
    """

    function7 = """
    点歌功能指令格式：
    
    1. [点歌 xxx]：默认点和xxx有关的第一首歌
    2. [点歌 xxx 0]：列出和xxx有关的所有歌曲条目
    3. [点歌 xxx 序号]：点第[序号]首歌
    
    示例：
    1. 点歌 爱我中华
    2. 点歌 爱我中华 0
    3. 点歌 爱我中华 2
    """

    function8 = """
    翻译功能指令格式：

    1. [翻译 xxx]：将xxx翻译成中文
    2. [翻译成aaa语 bbb]：将bbb翻译成aaa语
    
    示例：
    1. 翻译 good morning
    2. 翻译成日语 早上好
    """

    function9 = """
    毒鸡汤功能指令格式：

    [鸡汤/毒鸡汤/djt]
    """

    function10 = """
    土味情话功能指令格式：

    [情话/土味情话/twqh]
    """

    function11 = """
    舔狗日记功能指令格式：

    [日记/舔狗日记/tgrj]
    """

    function12 = """
    好好说话功能指令格式：

    [好好说话 xxx]：xxx为拼音缩写，该功能会查询和xxx缩写有关的词汇
    """

    function13 = """
    生成绝绝子功能指令格式：

    1. [生成绝绝子]：获得一段随机绝绝子
    2. [生成绝绝子 动词 名词]：以 [动词][名词] 为主题生成一段绝言绝语，示例：生成绝绝子 喝 奶茶
    """

    function14 = """
    生成记仇表情包功能指令格式：
    
    [记仇/小本本记下来/这仇我记下了/这个仇我记下了 xxx]：使用xxx生成一个记仇表情包

    示例：记仇 今天koi把我鸽了，这个仇我记下了
    """

    function15 = """
    cosplay图片指令格式：

    [cos/coser/cosplay]
    """

    function16 = """
    疫情数据查询指令格式：
    
    1. [疫情]：查询全国疫情概况
    2. [xxx疫情]：查询xxx地区（省、市级）的疫情情况，xxx中不需要加'省'或'市'的后缀
    
    示例：
    1. 疫情
    2. 浙江疫情
    3. 温州疫情
    """

    function17 = """
    投稿指令格式：

    [投稿 xxx]：将投稿内容xxx保存，将在周末展示投稿箱中的所有稿件
    
    tip: 该指令可在与bot的私聊中使用
    """

    # FORMAT THE OUTPUT
    @staticmethod
    def format(raw):
        return '\n'.join([line[4:] for line in raw[1:-5].split('\n')])

    # PROPERTY - CONTENT
    @staticmethod
    def main_content():
        return Menu.format(Menu._content)

    # SHOW FUNCTION DETAIL HELP
    @staticmethod
    def detail(seq):
        if not seq.isdigit():
            return Util.bot_invalid_input_response()
        if 1 <= int(seq) <= 17:
            return Menu.format(eval(f"Menu.function{seq}"))
        else:
            return Util.bot_invalid_input_response()
