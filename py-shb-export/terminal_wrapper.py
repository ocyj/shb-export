class TerminalWrapper:
    def __init__(self, f, use_tty = False):
        self.f = f
        self.line_count = 0

    def write(self, s):
        # Count newline characters in the string being written.
        if self.line_count > 0:
            self.f.print(f"\033[{self.line_count}A", end="")
            self.line_count = 0
        self.line_count += s.count('\n')
        return self.f.write(s)

    def flush(self):
        return self.f.flush()

    # Delegate attribute access to the original file
    def __getattr__(self, attr):
        return getattr(self.f, attr)
