import json
import sys

import segno

class TerminalWriter:
    def __init__(self):
        self._qr_out = sys.stderr
        self._data_out = sys.stdout
        self._line_count = 0


    def clear(self):
        self._qr_out.write("\033[2J")
        return self._qr_out.flush()


    def put_qr(self, data:str):
        qrcode = segno.make(data, micro=False)
        self.reset_qr_terminal()
        qrcode.terminal(out=self, border=1, compact=True)


    def put_json(self, data:dict):
        print(json.dumps(data, indent=2, ensure_ascii=False), file = self._data_out)


    def write(self, s):
        self._line_count += s.count('\n')
        return self._qr_out.write(s)


    # Delegate attribute access to the original file
    def __getattr__(self, attr):
        return getattr(self._qr_out, attr)


    def reset_qr_terminal(self):
        if self._line_count > 0:
            self._qr_out.write(f"\033[{self._line_count}A")
            self._line_count = 0