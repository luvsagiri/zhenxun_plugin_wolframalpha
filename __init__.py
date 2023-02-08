from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
)
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.internal.params import ArgStr
from nonebot.params import CommandArg
from nonebot.typing import T_State
from utils.message_builder import custom_forward_msg, image
from configs.config import NICKNAME, Config
import wolframalpha
import re

__zx_plugin_name__ = "wolframalpha"
__plugin_usage__ = """
usage：
    使用wolframalpha进行全能搜索
    wa/WA/wolframalpha +[内容]
"""
__plugin_version__ = 0.1
__plugin_author__ = "luvsagiri"
__plugin_settings__ = {
    "level": 5,
    "cmd": ["wa", "WA", "wolframalpha"],
}
__plugin_configs__ = {
    "wolframalpha_APPID": {"value": [], "help": "wolframalpha_APPID,请前往https://developer.wolframalpha.com/获取"},
}
__plugin_configs__ = {
    "wolframalpha_APPID": {
        "value": None,
        "help": "wolframalpha_APPID,请前往https://developer.wolframalpha.com/获取",
        "default_value": "",
    },
}

wa = on_command("wa", aliases={"WA", "wolframalpha"}, priority=5, block=True)

plugin_name = re.split(r'[\\/]', __file__)[-2]

@wa.handle()
async def _(state: T_State, arg: Message = CommandArg()):
    if arg.extract_plain_text().strip():
        state["question"] = arg.extract_plain_text().strip()


@wa.got("question", prompt="你想要知道什么？")
async def _(bot: Bot, event: MessageEvent, state: T_State, key_word: str = ArgStr("question")):
    replays = []
    app_id = Config.get_config(plugin_name, "wolframalpha_APPID")
    client = wolframalpha.Client(app_id)
    res = client.query(key_word)
    for pod in res.pods:
        result_sub = ''
        result_sub += pod.title
        for sub in pod.subpods:
            result_sub += image(sub.img.src)
            replays.append(result_sub)
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_forward_msg(
            group_id=event.group_id, messages=custom_forward_msg(replays, bot.self_id, f"全知全能{NICKNAME}")
        )
    else:
        for m in replays:
            await wa.send(m)
