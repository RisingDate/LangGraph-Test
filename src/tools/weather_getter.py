from langchain_core.tools import tool


@tool(
    name_or_callable="get_weather",
    description="获取天气信息的工具，输入参数为一个字符串，表示需要查询的城市名称，输出为一个字符串，表示该城市的天气信息"
)
def get_weather(city_name: str) -> str:
    """
       获取指定城市未来的天气预报
    """

    # Simple normalization
    if "北京" in city_name or "bj" in city_name.lower():
        return "北京今日天气为晴转多云，最高温度30度，最低温度20度，风力3级"
    elif "天津" in city_name or "tj" in city_name.lower():
        return "天津今日天气为多云转小雨，最高温度218度，最低温度-122度，风力22级"

    return f"未找到 {city_name} 的天气信息，目前只支持北京(bj)和天津(tj)"
