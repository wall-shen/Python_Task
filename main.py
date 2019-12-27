class PyMacroParser():
    def __init__(self):
        self.dict = {}
        self.lnNum = 0

    def preDeal(self, lines):
        line = lines[self.lnNum].strip()
        # deal with comment
        i = line.find("//")
        if i != -1:
            line = line[0:i]
            
        i = line.find("/*")
        while i != -1:
            end = line.find("*/", i+2)
            if end != -1:
                line = line[0:i] + line[end+2:]
                i = line.find("/*", i)
            else:
                line = line[0:i]
                while end == -1:
                    self.lnNum += 1
                    tLine = lines[self.lnNum].strip()
                    end = tLine.find("*/")
                    if end != -1:
                        lines[self.lnNum] = tLine[end+2:-1]
                        self.lnNum -= 1
                        i = -1
        self.lnNum += 1
        return line.split()

    def dealType(self, line):
        if line[0] == "'":
            line = ord(line[1])
        elif line[0] == '"':
            line = line[1:-1]
        elif line[0] == 'L':
            # change
            line = line[2: -1]
        elif line[:2] == "0x":
            line = int(line, 16)
        elif line[-1] == 'f':
            line = float(line[:-1])
        elif line == "true":
            line = True
        elif line == "false":
            line = False
        elif '.' in line:
            line = float(line)
        else:
            line = int(line)
        return line

    def dealTuple(self, line, pos):
        print(line)
        result = []
        while pos < len(line):
            if line[pos] == ' ':
                pos += 1
                pass
            elif line[pos] == '{':
                tResult, pos = self.dealTuple(line, pos+1)
                result.append(tResult)
            elif line[pos] == '}':
                pos += 1
                break
            elif line[pos] == ',':
                pos += 1
                pass
            else:
                endPos = line.find(',', pos)
                if endPos == -1:
                    endPos = len(line)
                tLine = line[pos:endPos]
                tPos = tLine.find('}')
                if tPos != -1:
                    tLine = line[pos:pos+tPos]
                    result.append(self.dealType(tLine))
                    pos = pos + tPos
                else:
                    result.append(self.dealType(tLine))
                    pos = endPos
        return result, pos

    def transform(self,line):
        print(line)
        if line[0] == "{":
            result, pos =  self.dealTuple(line, 0)
            return result[0]
        else:
            return self.dealType(line)
    
    def parse(self, lines, flagOut, flagIn):
        while self.lnNum < len(lines):
            line = self.preDeal(lines)
            if len(line) > 0:
                if line[0] == "#define" and flagOut and flagIn:
                    if len(line) == 2:
                        self.dict[line[1]] = None
                    else:
                        self.dict[line[1]] = self.transform(' '.join(line[2:]))
                elif line[0] == "#undef" and flagOut and flagIn:
                    if line[1] in self.dict.keys():
                        del self.dict[line[1]]
                elif line[0] == "#ifdef":
                    if line[1] in self.dict.keys():
                        self.parse(lines, flagOut and flagIn, True)
                    else:
                        self.parse(lines, flagOut and flagIn, False)
                elif line[0] == "#ifndef":
                    if line[1] in self.dict.keys():
                        self.parse(lines, flagOut and flagIn, False)
                    else:
                        self.parse(lines, flagOut and flagIn, True)
                elif line[0] == "#else":
                    flagIn = not flagIn
                elif line[0] == "#endif":
                    break

    def load(self, f):
        try:
            with open(f, encoding='UTF-8') as of:
                lines = of.readlines()
                self.parse(lines, True, True)
        except IOError:
            pass

    def preDefine(self, s):
        temp = s.split(';')
        self.dict = {}
        for i in temp:
            self.dict[i] = None

    def dumpDict(self):
        pass
    
    def demp(self, f):
        pass

    def show(self):
        print(self.dict)

p = PyMacroParser()
p.preDefine("MC1;MC2")
p.load("E:\code\PythonTask\.vscode\demo.txt")

p.show()

    