# -*- coding: utf-8 -*-

import re
from math import ceil

import arrow
import emoji
import requests
from PIL import Image, ImageDraw, ImageFont
from yaml import BaseLoader
from yaml import load as yload

from constant import (
    C_000000,
    C_6D4B2B,
    C_FFFFFF,
    EMOJIONE,
    GOTHICA1,
    HANNOTATESC_W5,
    HUAWENYUANTI_BOLD,
    HYQIHEI_AZEJ,
    MATHEMATICAL_ALPHANUMERIC_SYMBOLS,
    MODIFIER_LETTER,
    REDFM,
    SCRIPT_SIGN_SQUARE,
    SEGOE_UI,
    SEGOE_UI_SYMBOL,
    STYUANTI_SC_BOLD,
    TOP100IMG,
    YUME,
)

LOST_INFO = {
    "42": {
        "aid": "42",
        "bvid": "42",
        "tname": "42",
        "pubdate": 42,
        "owner": "42",
        "title": "42",
    }
}


def GetInfo(aid):
    result = requests.get(
        f"https://api.bilibili.com/x/web-interface/view?aid={aid}"
    ).json()
    if result["code"] != 0:
        return None
    else:
        infodata = {
            "aid": aid,
            "bvid": result["data"]["bvid"],
            "tname": result["data"]["tname"],
            "pubdate": result["data"]["pubdate"],
            "owner": result["data"]["owner"]["name"],
            "title": result["data"]["title"],
        }
        print(infodata)
        return infodata


def Single(Avid, Week):
    Author_F = ImageFont.truetype(HANNOTATESC_W5, 32)
    Bid_F = ImageFont.truetype(STYUANTI_SC_BOLD, 42)
    Cata_F = ImageFont.truetype(STYUANTI_SC_BOLD, 36)
    Emoji_F = ImageFont.truetype(EMOJIONE, 54)
    Title_F = ImageFont.truetype(HUAWENYUANTI_BOLD, 54)
    UnicodeA_F = ImageFont.truetype(SEGOE_UI, 54)
    UnicodeB_F = ImageFont.truetype(SEGOE_UI_SYMBOL, 54)
    UnicodeC_F = ImageFont.truetype(GOTHICA1, 54)
    Week_F = ImageFont.truetype(HYQIHEI_AZEJ, 41)
    YearCount_F = ImageFont.truetype(HYQIHEI_AZEJ, 20)
    RankTime_F = ImageFont.truetype(HUAWENYUANTI_BOLD, 38)
    UpTime_F = Cata_F
    AllData = GetInfo(Avid)
    if AllData is None:
        AllData = LOST_INFO[Avid]
    Aid = AllData["aid"]
    Author = AllData["owner"]
    Bid = AllData["bvid"]
    Cata = AllData["tname"]
    Title = AllData["title"]
    UpTime = arrow.get(AllData["pubdate"]).format("YYYY-MM-DD HH:mm")
    RankDate = arrow.get(Week * 7 * 24 * 3600 + YUME).shift(days=-1)
    RankTime = f"{RankDate.format('YYYY年M月')}第{ceil(int(RankDate.format('D'))/7)}周"
    RankImg = Image.open(TOP100IMG)
    RankPaper = ImageDraw.Draw(RankImg)

    if int(RankDate.format("M")) == 6 and ceil(int(RankDate.format("D")) / 7) == 4:
        FMImg = Image.open(REDFM)
        FMRegion = FMImg.crop((0, 0) + FMImg.size)
        FMCover = FMRegion.resize((326, 203), Image.ANTIALIAS)
        RankImg.paste(FMCover, (1542, 707))
        YearCount = int(RankDate.format("YYYY")) - 2009
        FMImg_X = 1560
        RankPaper.text(
            (FMImg_X + 1, 830 + 1), f"The {YearCount}th year", C_000000, YearCount_F
        )
        RankPaper.text((FMImg_X, 830), f"The {YearCount}th year", C_FFFFFF, YearCount_F)

    ShinkSize = 0
    Title_O = 31
    RegexTitle = re.sub(chr(65039), "", Title)
    while (Title_F.getsize(RegexTitle)[0] + Title_O) > 1440:
        ShinkSize += 1
        Title_F = ImageFont.truetype(HUAWENYUANTI_BOLD, 54 - ShinkSize)
        Emoji_F = ImageFont.truetype(EMOJIONE, 54 - ShinkSize)
        UnicodeA_F = ImageFont.truetype(SEGOE_UI, 54 - ShinkSize)
        UnicodeB_F = ImageFont.truetype(SEGOE_UI_SYMBOL, 54 - ShinkSize)
        UnicodeC_F = ImageFont.truetype(GOTHICA1, 54 - ShinkSize)

    i = 0
    Title_Step = Title_O
    while i < len(RegexTitle):
        if RegexTitle[i] in emoji.UNICODE_EMOJI["en"]:
            RankPaper.text((Title_Step, 979), RegexTitle[i], C_6D4B2B, Emoji_F)
            Title_Step += Emoji_F.getsize(RegexTitle[i])[0]
        elif re.match(SCRIPT_SIGN_SQUARE, RegexTitle[i]) is not None:
            RankPaper.text(
                (Title_Step, 979),
                RegexTitle[i],
                C_6D4B2B,
                UnicodeC_F,
            )
            Title_Step += UnicodeC_F.getsize(RegexTitle[i])[0]
        elif re.match(MATHEMATICAL_ALPHANUMERIC_SYMBOLS, RegexTitle[i]) is not None:
            RankPaper.text(
                (Title_Step, 979 - UnicodeB_F.getsize(RegexTitle[i])[1] * 0.15),
                RegexTitle[i],
                C_6D4B2B,
                UnicodeB_F,
            )
            Title_Step += UnicodeB_F.getsize(RegexTitle[i])[0]
        elif (
            (re.match(MODIFIER_LETTER, RegexTitle[i]) is not None)
            or (
                i + 1 < len(RegexTitle)
                and re.match(r"[0-9a-zA-Z\u4E00-\u9FA5]", RegexTitle[i + 1]) is None
                and re.match(MODIFIER_LETTER, RegexTitle[i + 1]) is not None
            )
            or (re.match(MODIFIER_LETTER, RegexTitle[i - 1]) is not None)
        ):
            RankPaper.text((Title_Step, 979), RegexTitle[i], C_6D4B2B, UnicodeA_F)
            Title_Step += UnicodeA_F.getsize(RegexTitle[i])[0]
        else:
            RankPaper.text((Title_Step, 979), RegexTitle[i], C_6D4B2B, Title_F)
            Title_Step += Title_F.getsize(RegexTitle[i])[0]
        i += 1

    Author_X = 31
    AuthorName = f"{Author}   投稿"
    RankPaper.text((Author_X, 927), AuthorName, C_6D4B2B, Author_F)
    Bid_X = 195 - Bid_F.getsize(Bid)[0] / 2
    RankPaper.text((Bid_X, 847), Bid, C_FFFFFF, Bid_F)
    Cata_X = 580 - Cata_F.getsize(Cata)[0] / 2
    RankPaper.text((Cata_X, 849), Cata, C_6D4B2B, Cata_F)
    UpTime_O = 933
    UpTime_X = UpTime_O - UpTime_F.getsize(UpTime)[0] / 2
    RankPaper.text((UpTime_X, 850), UpTime, C_6D4B2B, UpTime_F)
    Week_X = 1560
    RankPaper.text((Week_X + 1, 782 + 1), f"#{Week}", C_000000, Week_F)
    RankPaper.text((Week_X, 782), f"#{Week}", C_FFFFFF, Week_F)
    RankTime_X = 1705 - RankTime_F.getsize(RankTime)[0] / 2
    RankPaper.text((RankTime_X, 926), RankTime, C_FFFFFF, RankTime_F)
    RankImg.save(f"./ranking/list100/{Week}_av{Aid}.png")


def Main():
    ymlfile = yload(
        open(
            "./ranking/list100/100.yml",
            "r",
            encoding="utf-8-sig",
        ),
        Loader=BaseLoader,
    )
    for x in ymlfile:
        print(x[":name"][2:], 601 - int(x[":rank"]))
        Single(x[":name"][2:], 601 - int(x[":rank"]))


if __name__ == "__main__":
    Main()
