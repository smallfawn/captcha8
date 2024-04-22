from uuid import uuid4
from curl_cffi import requests
import ctypes
import json
import random
import urllib.parse
import execjs

js = execjs.compile(open("./index.js").read())

lookup = ["Z", "m", "s", "e", "r", "b", "B", "o", "H", "Q", "t", "N", "P", "+", "w", "O", "c", "z", "a", "/", "L", "p", "n", "g", "G", "8", "y", "J", "q", "4", "2", "K", "W", "Y", "j", "0", "D", "S", "f", "d", "i", "k", "x", "3", "V", "T", "1", "6", "I", "l", "U", "A", "F", "M", "9", "7", "h", "E", "C", "v", "u", "R", "X", "5",]


def tripletToBase64(e):
    return (
        lookup[63 & (e >> 18)] + lookup[63 & (e >> 12)] + lookup[(e >> 6) & 63] + lookup[e & 63]
    )


def encodeChunk(e, t, r):
    m = []
    for b in range(t, r, 3):
        n = (16711680 & (e[b] << 16)) + \
            ((e[b + 1] << 8) & 65280) + (e[b + 2] & 255)
        m.append(tripletToBase64(n))
    return ''.join(m)


def b64Encode(e):
    P = len(e)
    W = P % 3
    U = []
    z = 16383
    H = 0
    Z = P - W
    while H < Z:
        U.append(encodeChunk(e, H, Z if H + z > Z else H + z))
        H += z
    if 1 == W:
        F = e[P - 1]
        U.append(lookup[F >> 2] + lookup[(F << 4) & 63] + "==")
    elif 2 == W:
        F = (e[P - 2] << 8) + e[P - 1]
        U.append(lookup[F >> 10] + lookup[63 & (F >> 4)] + lookup[(F << 2) & 63] + "=")
    return "".join(U)


def encodeUtf8(e):
    b = []
    m = urllib.parse.quote(e, safe='~()*!.\'')
    w = 0
    while w < len(m):
        T = m[w]
        if T == "%":
            E = m[w + 1] + m[w + 2]
            S = int(E, 16)
            b.append(S)
            w += 2
        else:
            b.append(ord(T[0]))
        w += 1
    return b


def randhex(length):
    characters = "abcdef1234567890"
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


def mrc(e):
    ie = [
        0, 1996959894, 3993919788, 2567524794, 124634137, 1886057615, 3915621685,
        2657392035, 249268274, 2044508324, 3772115230, 2547177864, 162941995,
        2125561021, 3887607047, 2428444049, 498536548, 1789927666, 4089016648,
        2227061214, 450548861, 1843258603, 4107580753, 2211677639, 325883990,
        1684777152, 4251122042, 2321926636, 335633487, 1661365465, 4195302755,
        2366115317, 997073096, 1281953886, 3579855332, 2724688242, 1006888145,
        1258607687, 3524101629, 2768942443, 901097722, 1119000684, 3686517206,
        2898065728, 853044451, 1172266101, 3705015759, 2882616665, 651767980,
        1373503546, 3369554304, 3218104598, 565507253, 1454621731, 3485111705,
        3099436303, 671266974, 1594198024, 3322730930, 2970347812, 795835527,
        1483230225, 3244367275, 3060149565, 1994146192, 31158534, 2563907772,
        4023717930, 1907459465, 112637215, 2680153253, 3904427059, 2013776290,
        251722036, 2517215374, 3775830040, 2137656763, 141376813, 2439277719,
        3865271297, 1802195444, 476864866, 2238001368, 4066508878, 1812370925,
        453092731, 2181625025, 4111451223, 1706088902, 314042704, 2344532202,
        4240017532, 1658658271, 366619977, 2362670323, 4224994405, 1303535960,
        984961486, 2747007092, 3569037538, 1256170817, 1037604311, 2765210733,
        3554079995, 1131014506, 879679996, 2909243462, 3663771856, 1141124467,
        855842277, 2852801631, 3708648649, 1342533948, 654459306, 3188396048,
        3373015174, 1466479909, 544179635, 3110523913, 3462522015, 1591671054,
        702138776, 2966460450, 3352799412, 1504918807, 783551873, 3082640443,
        3233442989, 3988292384, 2596254646, 62317068, 1957810842, 3939845945,
        2647816111, 81470997, 1943803523, 3814918930, 2489596804, 225274430,
        2053790376, 3826175755, 2466906013, 167816743, 2097651377, 4027552580,
        2265490386, 503444072, 1762050814, 4150417245, 2154129355, 426522225,
        1852507879, 4275313526, 2312317920, 282753626, 1742555852, 4189708143,
        2394877945, 397917763, 1622183637, 3604390888, 2714866558, 953729732,
        1340076626, 3518719985, 2797360999, 1068828381, 1219638859, 3624741850,
        2936675148, 906185462, 1090812512, 3747672003, 2825379669, 829329135,
        1181335161, 3412177804, 3160834842, 628085408, 1382605366, 3423369109,
        3138078467, 570562233, 1426400815, 3317316542, 2998733608, 733239954,
        1555261956, 3268935591, 3050360625, 752459403, 1541320221, 2607071920,
        3965973030, 1969922972, 40735498, 2617837225, 3943577151, 1913087877,
        83908371, 2512341634, 3803740692, 2075208622, 213261112, 2463272603,
        3855990285, 2094854071, 198958881, 2262029012, 4057260610, 1759359992,
        534414190, 2176718541, 4139329115, 1873836001, 414664567, 2282248934,
        4279200368, 1711684554, 285281116, 2405801727, 4167216745, 1634467795,
        376229701, 2685067896, 3608007406, 1308918612, 956543938, 2808555105,
        3495958263, 1231636301, 1047427035, 2932959818, 3654703836, 1088359270,
        936918000, 2847714899, 3736837829, 1202900863, 817233897, 3183342108,
        3401237130, 1404277552, 615818150, 3134207493, 3453421203, 1423857449,
        601450431, 3009837614, 3294710456, 1567103746, 711928724, 3020668471,
        3272380065, 1510334235, 755167117,
    ]
    o = -1

    def right_without_sign(num: int, bit: int = 0) -> int:
        val = ctypes.c_uint32(num).value >> bit
        MAX32INT = 4294967295
        return (val + (MAX32INT + 1)) % (2 * (MAX32INT + 1)) - MAX32INT - 1

    for n in range(57):
        o = ie[(o & 255) ^ ord(e[n])] ^ right_without_sign(o, 8)
    return o ^ -1 ^ 3988292384


def encryptHeaders(url: str, data: dict, a1: str):
    # 加密xs,xt
    res = js.call("myEncrypt", url, data)
    x6, x7 = str(res["X-t"]), res["X-s"]

    # 浏览器指纹信息
    x8 = "浏览器指纹信息，自己获取"

    # 加密x-s-common
    mmm = {"s0": 3, "s1": "", "x0": "1", "x1": "3.6.8", "x2": "MacOS", "x3": "xhs-pc-web", "x4": "4.4.0", "x5": a1, "x6": x6, "x7": x7, "x8": x8, "x9": mrc(x6+x7+x8), "x10": 1}
    x_s_common = b64Encode(encodeUtf8(json.dumps(mmm)))

    # 组成headers
    headers = {
        "authority": "edith.xiaohongshu.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.xiaohongshu.com",
        "pragma": "no-cache",
        "referer": "https://www.xiaohongshu.com/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "x-b3-traceid": randhex(16),
        "x-s": x7,
        "x-s-common": x_s_common,
        "x-t": x6
    }
    return headers


def like(cookies: dict, NoteId: str):
    url = "https://edith.xiaohongshu.com/api/sns/web/v1/note/like"
    data = {"note_oid": NoteId}
    headers = encryptHeaders(url.split("xiaohongshu.com")[1], data, cookies["a1"])
    response = requests.post(url, headers=headers, cookies=cookies, json=data)
    print(response.json())
    return response.json()


def dislike(cookies: dict, NoteId: str):
    url = "https://edith.xiaohongshu.com/api/sns/web/v1/note/dislike"
    data = {"note_oid": NoteId}
    headers = encryptHeaders(url.split("xiaohongshu.com")[1], data, cookies["a1"])
    response = requests.post(url, headers=headers, cookies=cookies, json=data)
    print(response.json())
    return response.json()


def getNoteUserInfo(cookies: dict, user_id: str):
    url = f"https://edith.xiaohongshu.com/api/sns/web/v1/user/otherinfo?target_user_id={user_id}"
    headers = encryptHeaders(url.split("xiaohongshu.com")[1], None, cookies["a1"])
    response = requests.get(url, headers=headers, cookies=cookies)
    print(response.json())
    return response.json()


def getAllNoteByUserId(cookies: dict, user_id: str):
    url = f"https://edith.xiaohongshu.com/api/sns/web/v1/user_posted?num=220&cursor=&user_id={user_id}&image_formats=jpg,webp,avif"
    headers = encryptHeaders(url.split("xiaohongshu.com")[1], None, cookies["a1"])
    response = requests.get(url, headers=headers, cookies=cookies)
    print(response.json())
    return response.json()


# x参数为可变参数,自取
cookies = {
    "abRequestId": str(uuid4()),
    "a1": "x",
    "webId": "x",
    "gid": "x",
    "xsecappid": "xhs-pc-web",
    "web_session": "x",
    "webBuild": "4.4.0",
    "unread": "x",
    "acw_tc": "x",
    "websectiga": "x",
    "sec_poison_id": str(uuid4())
}
getAllNoteByUserId(cookies, "626f6bbe0000000010009a3d")
