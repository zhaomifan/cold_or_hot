from collections.abc import Generator
from enum import Enum, auto
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class ColdOrHotTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # 取第一个参数的值
        query = next(iter(tool_parameters.values()))
        # 判断语言
        language = "zh" if tool_parameters.get("language") == "zh" else "en"
        # 转换为枚举字符串
        cold_or_hot = ColdOrHot.from_value(hash(query))
        # 创建message
        cn_result = f"\"{query}\" 是 {cold_or_hot.value}"
        en_result = f"\"{query}\" is {cold_or_hot.name.lower()}"
        result = cn_result
        if language == "en":
            result = en_result
        yield self.create_json_message({
            "result": result,
            "cn_result": cn_result,
            "en_result": en_result,
        })


class ColdOrHot(Enum):
    COLD = "冷的"
    HOT = "热的"

    @classmethod
    def from_value(cls, value: int):
        return cls.COLD if value & 1 == 0 else cls.HOT


if __name__ == '__main__':
    e = ColdOrHot.from_value(1)
    print(e.name.lower())
    print(e.value)
