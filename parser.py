class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def lookahead(self):
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None

    def advance(self):
        self.pos += 1

    def expect(self, expected_type):
        token = self.current_token()
        if token and token[0] == expected_type:
            self.advance()
        else:
            raise Exception(f"Esperado '{expected_type}', mas encontrado: {token}")

    def parse_programa(self):
        while self.current_token():
            self.parse_declaracao()

    def parse_declaracao(self):
        token = self.current_token()
        if token[0] in {"INT", "FLOAT", "CHAR", "BOOLEAN", "VOID"}:
            self.parse_declaracao_variavel_ou_funcao()
        elif token[0] == "COMMENT":
            self.advance()
        elif token[0] in {"IF", "WHILE", "FOR", "RETURN"}:
            self.parse_estrutura_controle()
        elif token[0] == "SCANF":
            self.parse_scanf()
        elif token[0] == "PRINTLN":
            self.parse_println()
        else:
            raise Exception(f"Declaração inválida iniciada por {token}")

    def parse_declaracao_variavel_ou_funcao(self):
        self.parse_tipo()
        self.expect("ID")
        if self.current_token() and self.current_token()[0] == "(":
            self.parse_declaracao_funcao()
        else:
            self.parse_declaracao_variavel()

    def parse_tipo(self):
        token = self.current_token()
        if token and token[0] in {"INT", "FLOAT", "CHAR", "BOOLEAN", "VOID"}:
            self.advance()
        else:
            raise Exception(f"Tipo inválido: {token}")

    def parse_declaracao_variavel(self):
        token = self.current_token()
        if token and token[0] == "0":
            self.advance()
            self.parse_expressao()
        self.expect(";")

    def parse_declaracao_funcao(self):
        self.expect("(")
        self.parse_parametros()
        self.expect(")")
        self.parse_bloco()
    
    def parse_scanf(self):
        self.expect("SCANF")
        self.expect("(")
        self.expect("ID")
        self.expect(")")
        self.expect(";")

    def parse_println(self):
        self.expect("PRINTLN")
        self.expect("(")
        if self.current_token() and self.current_token()[0] in {"ID", "NUM_INT", "NUM_DEC", "TEXTO", "("}:
            self.parse_expressao()
        self.expect(")")
        self.expect(";")


    def parse_parametros(self):
        token = self.current_token()
        if not token or token[0] == ")":
            return
        self.parse_parametro()
        while self.current_token() and self.current_token()[0] == ",":
            self.advance()
            self.parse_parametro()


    def parse_parametro(self):
        self.parse_tipo()
        self.expect("ID")

    def parse_bloco(self):
        self.expect("{")
        while self.current_token() and self.current_token()[0] != "}":
            self.parse_declaracao()
        self.expect("}")

    def parse_estrutura_controle(self):
        token = self.current_token()
        if token[0] == "IF":
            self.advance()
            self.expect("(")
            self.parse_expressao()
            self.expect(")")
            self.parse_bloco()
            if self.current_token() and self.current_token()[0] == "ELSE":
                self.advance()
                self.parse_bloco()
        elif token[0] == "WHILE":
            self.advance()
            self.expect("(")
            self.parse_expressao()
            self.expect(")")
            self.parse_bloco()
        elif token[0] == "RETURN":
            self.advance()
            self.parse_expressao()
            self.expect(";")
        elif token[0] == "FOR":
            self.advance()
            self.expect("(")
            self.parse_expressao()
            self.expect(";")
            self.parse_expressao()
            self.expect(";")
            self.parse_expressao()
            self.expect(")")
            self.parse_bloco()
        else:
            raise Exception(f"Estrutura de controle não suportada: {token}")

    def parse_expressao(self):
        esquerda = self.parse_termo_str()
        while self.current_token() and self.current_token()[0] in {"+", "-", "&&", "||"}:
            op = self.__str_token(self.current_token())
            self.advance()
            direita = self.parse_termo_str()
            esquerda += f" {op} {direita}"

        if self.current_token() and self.current_token()[0] == "COMP":
            comp_op = self.__str_token(self.current_token())
            self.advance()
            direita = self.parse_termo_str()
            esquerda += f" {comp_op} {direita}"

        print("Expressão:", esquerda)
        return esquerda

    def parse_termo_str(self):
        termo = self.parse_fator_str()
        while self.current_token() and self.current_token()[0] in {"*", "/", "%"}:
            op = self.__str_token(self.current_token())
            self.advance()
            fator = self.parse_fator_str()
            termo += f" {op} {fator}"
        return termo

    def parse_fator_str(self):
        token = self.current_token()

        if token[0] == "!":
            self.advance()
            fator = self.parse_fator_str()
            return f"!{fator}"
        if token[0] in {"ID", "NUM_INT", "NUM_DEC", "TEXTO"}:
            self.advance()
            return token[1]
        elif token[0] == "(":
            self.advance()
            inner = self.parse_termo_str()
            self.expect(")")
            return f"({inner})"
        else:
            raise Exception(f"Esperado valor primário, encontrado: {token}")


    def __str_token(self, token):
        if token:
            return token[1]
        return "EOF"
