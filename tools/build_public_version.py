#!/usr/bin/env python3
"""从本地完整版生成可上传公开仓库的脱敏 HTML。"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "peru_itinerary_2026_private.html"
TARGET = ROOT / "peru_itinerary_2026.html"


PUBLIC_DAYS = [
    """<div class="story-days public-story-days">
          <article class="story-day"><div class="story-date"><strong>09.22</strong><span>周二 · DAY 01</span></div><div class="story-day-body"><h3>上海 → 巴黎</h3><p>21:30从上海浦东出发，搭乘法航，经巴黎戴高乐机场转机前往利马。</p><p class="note">国际段最终以出票行程单为准。</p></div></article>
          <article class="story-day"><div class="story-date"><strong>09.23</strong><span>周三 · DAY 02</span></div><div class="story-day-body"><h3>抵达Lima，入住Miraflores</h3><ul class="day-list"><li><time>15:40</time> 抵达LIM，完成入境和取行李。</li><li><time>17:15-17:40</time> 完成行李整理与后续衔接，具体寄存安排仅向确认成员提供。</li><li><time>17:40-19:00</time> 预约车前往Miraflores，晚高峰按45-90分钟预留。</li><li><time>19:30-20:30</time> Larcomar → Malecón海岸步道 → Parque del Amor，之后在Miraflores简单晚餐。</li></ul><p class="note">抵达时已过日落，这段散步只用于透气和适应时差；体力不足可直接取消。</p><p class="stay"><strong>住宿</strong> Miraflores市区特色住宿，具体名称与地址仅向确认成员提供。</p></div></article>
          <article class="story-day"><div class="story-date"><strong>09.24</strong><span>周四 · DAY 03</span></div><div class="story-day-body"><h3>Lima历史、考古与城市空间日</h3><ul class="day-list"><li><time>10:00-10:55</time> San Francisco修道院与地下墓穴；随后步行看La Soledad、主教座堂、总主教宫和Santo Domingo外立面。</li><li><time>12:00-14:45</time> Larco Café轻午餐，参观Museo Larco的陶器、金属、纺织与展陈空间。</li><li><time>15:20-16:25</time> Huaca Pucllana预约导览，观察土坯金字塔及其与现代城区的尺度关系。</li><li><time>16:45-18:10</time> LUM室内展览与建筑，闭馆后在馆外公共海崖平台等待日落。</li></ul><p class="note">全天使用同一辆包车；LUM室内18:00关闭，日落属于馆外公共空间。</p><p class="stay"><strong>住宿</strong> Barranco历史街区特色住宿，具体名称与地址仅向确认成员提供。</p></div></article>
        </div>""",
    """<div class="story-days public-story-days">
          <article class="story-day"><div class="story-date"><strong>09.25</strong><span>周五 · DAY 04</span></div><div class="story-day-body"><h3>Lima → Puerto Maldonado → Tambopata</h3><ul class="day-list"><li><time>07:10</time> 从Barranco出发，约08:20在LIM取回两件主箱并办理国内航班托运。</li><li>目标航班为<time>10:20-12:05</time> LIM → PEM的LATAM直飞。</li><li>由营地接机；大箱由接待团队妥善保管，只带每人约10kg过夜包乘车与船进入营地。</li><li>约13:30午餐，下午Trail System雨林步道，晚餐后参加River Night Watch。</li></ul><p class="note">付款前书面确认机场接送、大箱保管、9月27日取件送机与航班衔接。</p><p class="stay"><strong>住宿</strong> 亚马逊生态营地 · 3天2晚套餐第1晚，具体名称与地址仅向确认成员提供。</p></div></article>
          <article class="story-day"><div class="story-date"><strong>09.26</strong><span>周六 · DAY 05</span></div><div class="story-day-body"><h3>Tambopata雨林全天</h3><ul class="day-list"><li>清晨按lodge安排早餐与观鸟，跟随天气和动物活动调整出发时间。</li><li>上午参加Canopy Walkway，在树冠吊桥和观察平台寻找鸟类与猴群。</li><li>下午优先申请将基础River Island替换为Lake Sandoval，结合雨林步行与湖面观察。</li><li>晚餐后参加Rainforest by Night，关闭闪光灯并完全服从向导。</li></ul><p class="note">Lake Sandoval能否替换、是否加价，以及天气取消后的替代活动均需书面确认。</p><p class="stay"><strong>住宿</strong> 亚马逊生态营地 · 套餐第2晚，具体名称与地址仅向确认成员提供。</p></div></article>
        </div>""",
    """<div class="story-days public-story-days">
          <article class="story-day"><div class="story-date"><strong>09.27</strong><span>周日 · DAY 06</span></div><div class="story-day-body"><h3>Tambopata → Cusco</h3><p>离开低海拔雨林进入安第斯高原，在库斯科放慢节奏，优先休息并适应海拔。</p><p class="stay"><strong>住宿</strong> 库斯科历史中心特色住宿，具体信息仅向确认成员提供。</p></div></article>
          <article class="story-day"><div class="story-date"><strong>09.28</strong><span>周一 · DAY 07</span></div><div class="story-day-body"><h3>Cusco → Chinchero → Moray → Maras → Ollantaytambo</h3><p>串联圣谷四处代表性现场，看梯田、纺织、盐田、巨石建筑和仍在生活的印加古镇。</p><p class="stay"><strong>住宿</strong> 圣谷历史型特色住宿，具体信息仅向确认成员提供。</p></div></article>
        </div>""",
    """<div class="story-days public-story-days">
          <article class="story-day"><div class="story-date"><strong>09.29</strong><span>周二 · DAY 08</span></div><div class="story-day-body"><h3>Ollantaytambo ↔ Machu Picchu → Cusco</h3><p>搭乘观景火车进入乌鲁班巴河谷，完整游览马丘比丘经典 Circuit 2，随后返回库斯科。</p><p class="stay"><strong>住宿</strong> 库斯科历史中心特色住宿，具体信息仅向确认成员提供。</p></div></article>
        </div>""",
    """<div class="story-days public-story-days">
          <article class="story-day"><div class="story-date"><strong>09.30</strong><span>周三 · DAY 09</span></div><div class="story-day-body"><h3>Cusco → Puno</h3><p>乘坐 PeruRail Titicaca Train 穿越安第斯高原与 La Raya，在观景车厢中度过完整的高原列车日。</p><p class="stay"><strong>住宿</strong> Puno 市区特色住宿，具体信息仅向确认成员提供。</p></div></article>
          <article class="story-day"><div class="story-date"><strong>10.01</strong><span>周四 · DAY 10</span></div><div class="story-day-body"><h3>Lake Titicaca：Uros + Taquile</h3><p>乘船走访 Uros 芦苇浮岛与 Taquile Island，在湖上看日落，并从湖光与雪山之间醒来。</p><p class="stay"><strong>住宿</strong> 的的喀喀湖上特色住宿，具体信息仅向确认成员提供。</p></div></article>
        </div>""",
    """<div class="story-days public-story-days">
          <article class="story-day"><div class="story-date"><strong>10.02</strong><span>周五 · DAY 11</span></div><div class="story-day-body"><h3>Uros → Puno → Arequipa</h3><p>离开高原湖泊前往白城 Arequipa，抵达后从 Plaza de Armas 与火山石街区开始认识城市。</p><p class="stay"><strong>住宿</strong> Arequipa 历史中心特色住宿，具体信息仅向确认成员提供。</p></div></article>
          <article class="story-day"><div class="story-date"><strong>10.03</strong><span>周六 · DAY 12</span></div><div class="story-day-body"><h3>Arequipa 火山石建筑日</h3><p>走进火山凝灰岩采石场与 Santa Catalina 修道院，傍晚在 Yanahuara 等待 Misti 火山方向的日落。</p><p class="stay"><strong>住宿</strong> Arequipa 历史中心特色住宿，具体信息仅向确认成员提供。</p></div></article>
        </div>""",
    """<div class="story-days public-story-days">
          <article class="story-day"><div class="story-date"><strong>10.04</strong><span>周日 · DAY 13</span></div><div class="story-day-body"><h3>Arequipa → Lima</h3><p>返回利马，在 Barranco 参观宅邸、艺术收藏并体验下午茶。</p><p class="stay"><strong>住宿</strong> Barranco 历史街区特色住宿，具体信息仅向确认成员提供。</p></div></article>
          <article class="story-day"><div class="story-date"><strong>10.05</strong><span>周一 · DAY 14</span></div><div class="story-day-body"><h3>Barranco 步行 + Central 午餐 → 返程</h3><p>以 Barranco 街区漫步和 Central tasting menu 收尾，随后前往机场启程回国。</p></div></article>
          <article class="story-day"><div class="story-date"><strong>10.06</strong><span>周二 · DAY 15</span></div><div class="story-day-body"><h3>巴黎国际中转</h3><p>按联程安排在巴黎完成国际中转，继续飞往上海。</p></div></article>
          <article class="story-day"><div class="story-date"><strong>10.07</strong><span>周三 · DAY 16</span></div><div class="story-day-body"><h3>抵达上海</h3><p>抵达上海，结束从亚马逊雨林到安第斯高原的秘鲁旅程。</p></div></article>
        </div>""",
]


def build_public(source: str) -> str:
    html = source

    html = html.replace("<title>秘鲁旅行计划 · 2026</title>", "<title>秘鲁旅行计划 · 2026｜公开版</title>")
    story_pattern = re.compile(
        r'<div class="story-days">.*?</div>\s*</div>\s*(?=<aside)', re.S
    )
    matches = list(story_pattern.finditer(html))
    if len(matches) != len(PUBLIC_DAYS):
        raise RuntimeError(f"应找到 {len(PUBLIC_DAYS)} 个行程章节，实际找到 {len(matches)} 个")

    index = 0

    def redact_story(story: str) -> str:
        story = re.sub(
            r'<p class="stay">.*?</p>',
            '<p class="stay"><strong>住宿</strong> 当地特色住宿，具体名称与地址仅向确认成员提供。</p>',
            story,
            flags=re.S,
        )
        replacements = {
            "鲁米旁库酒店 Hotel Rumi Punku": "库斯科市区住宿",
            "鲁米旁库酒店": "库斯科市区住宿",
            "鲁米旁库": "库斯科市区住宿",
            "Hotel Rumi Punku": "库斯科市区住宿",
            "Inkaterra书面确认": "营地团队书面确认",
            "El Albergue": "圣谷住宿",
            "Conde de Lemos": "Puno市区住宿",
            "Uros Titicaca Kurmi Lodge": "湖上住宿",
            "Uros Kurmi": "湖上住宿",
            "Palacio Guaqui": "Arequipa市区住宿",
            "Casa Republica Barranco Boutique Hotel": "Barranco市区住宿",
            "Casa Republica Barranco": "Barranco市区住宿",
            "Casa Republica": "Barranco市区住宿",
            "回到Puerto Maldonado后取回两件大箱": "离开雨林后完成大件行李衔接",
            "同时确认9月28日退房后寄存大箱、9月29日晚再次入住时取回": "同时确认进入圣谷前后的行李衔接",
            "两件大箱留在酒店，只带小型过夜包": "妥善安置两件大箱，只带小型过夜包",
            "退房后把小型过夜包寄存在圣谷住宿": "退房后妥善安置小型过夜包",
            "取包后由司机接站": "完成行李衔接后由司机接站",
            "回到库斯科市区住宿并取回大箱": "回到库斯科并完成行李衔接",
        }
        for original, public in replacements.items():
            story = story.replace(original, public)
        return story

    def replace_story(match: re.Match[str]) -> str:
        nonlocal index
        if index < 2:
            replacement = PUBLIC_DAYS[index] + "\n        </div>\n        "
        else:
            replacement = redact_story(match.group(0))
        index += 1
        return replacement

    html = story_pattern.sub(replace_story, html)

    html = re.sub(
        r'<tr><th>住宿</th><td>.*?</td></tr>',
        '<tr><th>住宿</th><td>全程 12 晚，覆盖城市设计型住宿、雨林生态营地、圣谷历史型住宿与的的喀喀湖上住宿；具体名称、地址和房型仅向确认成员提供。</td></tr>',
        html,
        count=1,
        flags=re.S,
    )
    html = html.replace(
        "Inkaterra Amazon Field Station 3天2晚",
        "亚马逊生态营地 3天2晚",
    )

    html = html.replace(
        "既能完整查看执行细节，也能顺着图片理解旅程的情绪变化。",
        "公开版展示完整时间线与执行安排；住宿名称、地址和具体寄存地点仅向确认成员提供。",
    )
    html = html.replace(
        "行程版本：2026-07 · 所有日期与交通均为暂定安排，最终以出票和确认订单为准。",
        "行程版本：2026-07 · 公开展示版 · 日期与路线为暂定安排，住宿及寄存地点仅向确认成员提供。",
    )

    forbidden = [
        "Hotel Indigo Lima Miraflores",
        "Viajero Lima - Barranco Hostel",
        "Inkaterra Amazon Field Station",
        "Hotel Rumi Punku",
        "El Albergue · Estación de Tren",
        "Conde de Lemos",
        "Uros Titicaca Kurmi Lodge",
        "Palacio Guaqui",
        "Casa Republica Barranco Boutique Hotel",
        "Calle Choquechaca 339",
        "Calle Alcanfores 1332",
        "Jirón Sáenz Peña 208",
        "寄存两件主箱",
    ]
    leaked = [item for item in forbidden if item in html]
    if leaked:
        raise RuntimeError("公开版仍包含敏感信息：" + "、".join(leaked))

    return html


if __name__ == "__main__":
    if not SOURCE.exists():
        raise SystemExit(f"找不到本地完整版：{SOURCE}")
    public_html = build_public(SOURCE.read_text(encoding="utf-8"))
    TARGET.write_text(public_html, encoding="utf-8")
    print(f"已生成公开版：{TARGET}")
