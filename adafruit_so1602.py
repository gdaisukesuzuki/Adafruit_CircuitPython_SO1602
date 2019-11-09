#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from time import sleep
try:
    import struct
except ImportError:
    import ustruct as struct
from micropython import const

__version__ = "0.0.0-auto.0"
#__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BMP280.git"
__repo__ = "dummy"

_REGISTER_CMD  = const(0x00)
_REGISTER_DATA = const(0x40)

_CMD_CURSOR_0 = const(0x80)
_CMD_CURSOR_1 = const(0xa0)
_CMD_DSP_CLR  = const(0x01)
_CMD_RET_HOME = const(0x02)
_CMD_DSP_ON_C0B0 = const(0x0c)
_CMD_DSP_ON_C0B1 = const(0x0d)
_CMD_DSP_ON_C1B0 = const(0x0e)
_CMD_DSP_ON_C1B1 = const(0x0f)
_CMD_DSP_OFF     = const(0x08)

_CHAR_TABLE = {
    u'†': [0x11],
    u'§': [0x12],
    u'¶': [0x13],
    u'Γ': [0x14],
    u'Δ': [0x15],
    u'θ': [0x16],
    u'Λ': [0x17],
    u'Ξ': [0x18],
    u'Π': [0x19],
    u'Σ': [0x1a],
    u'Φ': [0x1c],
    u'Ψ': [0x1d],
    u'Ω': [0x1e],
    u'α': [0x1f],

    u' ': [0x20],
    u'!': [0x21],
    u'"': [0x22],
    u'#': [0x23],
    u'$': [0x24],
    u'%': [0x25],
    u'&': [0x26],
    u"'": [0x27],
    u'(': [0x28],
    u')': [0x29],
    u'*': [0x2a],
    u'+': [0x2b],
    u',': [0x2c],
    u'-': [0x2d],
    u'.': [0x2e],
    u'/': [0x2f],

    u'0': [0x30],
    u'1': [0x31],
    u'2': [0x32],
    u'3': [0x33],
    u'4': [0x34],
    u'5': [0x35],
    u'6': [0x36],
    u'7': [0x37],
    u'8': [0x38],
    u'9': [0x39],
    u':': [0x3a],
    u';': [0x3b],
    u'<': [0x3c],
    u'=': [0x3d],
    u'>': [0x3e],
    u'?': [0x3f],

    u'@': [0x40],
    u'A': [0x41],
    u'B': [0x42],
    u'C': [0x43],
    u'D': [0x44],
    u'E': [0x45],
    u'F': [0x46],
    u'G': [0x47],
    u'H': [0x48],
    u'I': [0x49],
    u'J': [0x4a],
    u'K': [0x4b],
    u'L': [0x4c],
    u'M': [0x4d],
    u'N': [0x4e],
    u'O': [0x4f],

    u'P': [0x50],
    u'Q': [0x51],
    u'R': [0x52],
    u'S': [0x53],
    u'T': [0x54],
    u'U': [0x55],
    u'V': [0x56],
    u'W': [0x57],
    u'X': [0x58],
    u'Y': [0x59],
    u'Z': [0x5a],
    u'[': [0x5b],
    u'¥': [0x5c],
    u']': [0x5d],
    u'^': [0x5e],
    u'_': [0x5f],

    u'`': [0x60],
    u'a': [0x61],
    u'b': [0x62],
    u'c': [0x63],
    u'd': [0x64],
    u'e': [0x65],
    u'f': [0x66],
    u'g': [0x67],
    u'h': [0x68],
    u'i': [0x69],
    u'j': [0x6a],
    u'k': [0x6b],
    u'l': [0x6c],
    u'm': [0x6d],
    u'n': [0x6e],
    u'o': [0x6f],

    u'p': [0x70],
    u'q': [0x71],
    u'r': [0x72],
    u's': [0x73],
    u't': [0x74],
    u'u': [0x75],
    u'v': [0x76],
    u'w': [0x77],
    u'x': [0x78],
    u'y': [0x79],
    u'z': [0x7a],
    u'{': [0x7b],
    u'|': [0x7c],
    u'}': [0x7d],
    u'→': [0x7e],
    u'←': [0x7f],

    u'。': [0xa1],
    u'「': [0xa2],
    u'」': [0xa3],
    u'、': [0xa4],
    u'・': [0xa5],
    u'ヲ': [0xa6],
    u"ァ": [0xa7],
    u'ィ': [0xa8],
    u'ゥ': [0xa9],
    u'ェ': [0xaa],
    u'ォ': [0xab],
    u'ャ': [0xac],
    u'ュ': [0xad],
    u'ョ': [0xae],
    u'ッ': [0xaf],

    u'ー': [0xb0],
    u'ア': [0xb1],
    u'イ': [0xb2],
    u'ウ': [0xb3],
    u'エ': [0xb4],
    u'オ': [0xb5],
    u'カ': [0xb6],
    u'キ': [0xb7],
    u'ク': [0xb8],
    u'ケ': [0xb9],
    u'コ': [0xba],
    u'サ': [0xbb],
    u'シ': [0xbc],
    u'ス': [0xbd],
    u'セ': [0xbe],
    u'ソ': [0xbf],

    u'タ': [0xc0],
    u'チ': [0xc1],
    u'ツ': [0xc2],
    u'テ': [0xc3],
    u'ト': [0xc4],
    u'ナ': [0xc5],
    u'ニ': [0xc6],
    u'ヌ': [0xc7],
    u'ネ': [0xc8],
    u'ノ': [0xc9],
    u'ハ': [0xca],
    u'ヒ': [0xcb],
    u'フ': [0xcc],
    u'ヘ': [0xcd],
    u'ホ': [0xce],
    u'マ': [0xcf],

    u'ミ': [0xd0],
    u'ム': [0xd1],
    u'メ': [0xd2],
    u'モ': [0xd3],
    u'ヤ': [0xd4],
    u'ユ': [0xd5],
    u'ヨ': [0xd6],
    u'ラ': [0xd7],
    u'リ': [0xd8],
    u'ル': [0xd9],
    u'レ': [0xda],
    u'ロ': [0xdb],
    u'ワ': [0xdc],
    u'ン': [0xdd],
    u'゛': [0xde],
    u'゜': [0xdf],

    u'＇':[0xf0],
    u'"':[0xf1],
    u'°':[0xf2],
    u'×': [0xf7],
    u'÷': [0xf8],
    u'≧': [0xf9],
    u'≦': [0xfa],
    u'≪': [0xfb],
    u'≫': [0xfc],
    u'≠': [0xfd],
    u'√': [0xfe],
    u'￣': [0xff],

    u'ガ': [0xb6, 0xde],
    u'ギ': [0xb7, 0xde],
    u'グ': [0xb8, 0xde],
    u'ゲ': [0xb9, 0xde],
    u'ゴ': [0xba, 0xde],
    u'ザ': [0xbb, 0xde],
    u'ジ': [0xbc, 0xde],
    u'ズ': [0xbd, 0xde],
    u'ゼ': [0xbe, 0xde],
    u'ゾ': [0xbf, 0xde],
    u'ダ': [0xc0, 0xde],
    u'ヂ': [0xc1, 0xde],
    u'ヅ': [0xc2, 0xde],
    u'デ': [0xc3, 0xde],
    u'ド': [0xc4, 0xde],
    u'バ': [0xca, 0xde],
    u'ビ': [0xcb, 0xde],
    u'ブ': [0xcc, 0xde],
    u'ベ': [0xcd, 0xde],
    u'ボ': [0xce, 0xde],
    u'パ': [0xca, 0xdf],
    u'ピ': [0xcb, 0xdf],
    u'プ': [0xcc, 0xdf],
    u'ペ': [0xcd, 0xdf],
    u'ポ': [0xce, 0xdf],
}


class Adafruit_SO1602():
    def __init__(self, cursor, blink):
        self.displayClear()
        self.returnHome()
        self.displayOn(cursor, blink)
        self.displayClear()

    def writeLine(self, str = '', line = 0, align = 'left'):
        # while (len(str) < 16):
        #    if (align == 'right'):
        #        str = ' ' + str
        #    else:
        #        str = str + ' '

        str_enc = []
        for c in str:
            str_enc += _CHAR_TABLE[c]

        sleep(0.1)

        if (line == 1):
            self._write_register_byte(_REGISTER_CMD,_CMD_CURSOR_1)
            sleep(0.05)
        else:
            self._write_register_byte(_REGISTER_CMD,_CMD_CURSOR_0)

        while (len(str_enc) < 16):
            if (align == 'right'):
                str_enc = [0x20] + str_enc
            else:
                str_enc = str_enc + [0x20]


        for i in range(16):
            self._write_register_byte(_REGISTER_DATA,str_enc[i])

    def displayClear(self):
        self._write_register_byte(_REGISTER_CMD,_CMD_DSP_CLR)
    
    def returnHome(self):
        self._write_register_byte(_REGISTER_CMD,_CMD_RET_HOME)

    def displayOn(self, cursor = False, blink = False):
        if cursor:
            if blink:
                self._write_register_byte(_REGISTER_CMD,_CMD_DSP_ON_C1B1)
            else:
                self._write_register_byte(_REGISTER_CMD,_CMD_DSP_ON_C1B0)
        else:
            if blink:
                self._write_register_byte(_REGISTER_CMD,_CMD_DSP_ON_C0B1)
            else:
                self._write_register_byte(_REGISTER_CMD,_CMD_DSP_ON_C0B0)

    def displayOff(self):
        self._write_register_byte(_REGISTER_CMD,_CMD_DSP_OFF)

    def _read_register(self, register, length):
        """Low level register reading, not implemented in base class"""
        raise NotImplementedError()

    def _write_register_byte(self, register, value):
        """Low level register writing, not implemented in base class"""
        raise NotImplementedError()


class Adafruit_SO1602_I2C(Adafruit_SO1602): # pylint: disable=invalid-name
    """Driver for I2C connected BMP280. Default address is 0x77 but another address can be passed
       in as an argument"""
    def __init__(self, i2c, address=0x3c, cursor = False,blink = False):
        import adafruit_bus_device.i2c_device as i2c_device
        self._i2c = i2c_device.I2CDevice(i2c, address)
        super().__init__(cursor = cursor, blink = blink)

    def _read_register(self, register, length):
        """Low level register reading over I2C, returns a list of values"""
        with self._i2c as i2c:
            i2c.write(bytes([register & 0xFF]))
            result = bytearray(length)
            i2c.readinto(result)
            #print("$%02X => %s" % (register, [hex(i) for i in result]))
            return result

    def _write_register_byte(self, register, value):
        """Low level register writing over I2C, writes one 8-bit value"""
        with self._i2c as i2c:
            i2c.write(bytes([register & 0xFF, value & 0xFF]))
            #print("$%02X <= 0x%02X" % (register, value))


