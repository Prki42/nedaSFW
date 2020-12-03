from db import DatabaseConnection

class LatexCreator:
    def __init__(self, mysqldb: DatabaseConnection, sqlPath: str, templatePath: str, outputPath: str):
        self.mysqldb = mysqldb
        self.sqlPath = sqlPath
        self.templatePath = templatePath
        self.outputPath = outputPath

    def _extractFromSql(self, sqlFile) -> dict:
        queryDict = {}
        currNum = ""
        queryBuffer = ""
        for line in sqlFile:
            if line.isspace() : continue
            if line.startswith("#"):
                currNum = line[1:]
                continue
            queryBuffer += line
            if line.endswith(";\n") or line.endswith(";"):
                queryDict[currNum] = queryBuffer
                queryBuffer = ""
        return queryDict
    
    def _startSection(self, outputFile, heading: str):
        if heading.endswith("\n") : heading = heading[:-1]
        outputFile.write("\\section*{%s}\n" % (heading))
    
    def _writeCode(self, outputFile, codeWrap: str, code: str):
        outputFile.write(codeWrap % (code))
    
    # TODO Uradi ovo malo bolje
    def _writeTable(self, outputFile, data: list, columns: tuple):
        texCode = "\\begin{center}\n\\begin{tabular}{||"
        for _ in range(len(columns)) : texCode += " c|"
        texCode += "|}\n\\hline\n"
        for col in columns: texCode += str(col) + " & "
        texCode = texCode.replace("_", "\\_")
        texCode = texCode[:-2] + " \\\\ \n\\hline\\hline\n"
        outputFile.write(texCode)
        for row in data:
            texCode = ""
            for el in row:
                texCode += str(el) + " & "
            texCode = texCode.replace("_", "\\_")
            texCode = texCode[:-2] + " \\\\ \n\\hline\n"
            outputFile.write(texCode)
        outputFile.write("\\end{tabular}\n\\end{center}\n")

    def write(self, codeWrap: str, indicator: str):
        sqlFile = open(self.sqlPath, "r", encoding="utf-8")
        templateFile = open(self.templatePath, "r", encoding="utf-8")
        outputFile = open(self.outputPath, "w", encoding="utf-8")

        for line in templateFile:
            if indicator in line:
                break
            outputFile.write(line)

        queryDict = self._extractFromSql(sqlFile)
        sqlFile.close()
        for queryKey in queryDict:
            try:
                result, columns = self.mysqldb.executeQuery(queryDict[queryKey])
                self._startSection(outputFile, queryKey)
                self._writeCode(outputFile, codeWrap, queryDict[queryKey])
                self._writeTable(outputFile, result, columns)
            except Exception as e:
                print("Erro executing %s" % (queryKey))
                print(e)
        for line in templateFile : outputFile.write(line)
        templateFile.close()
        outputFile.close()
