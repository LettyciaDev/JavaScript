from parser import Parser

def main():
    # Leitura dos tokens do arquivo
    with open("entrada_tokens.txt", "r") as f:
        tokens = [line.strip().split() for line in f if line.strip()]
        # tokens como lista de (categoria, lexema)
    parser = Parser(tokens)
    try:
        parser.parse_programa()
        print("Análise sintática concluída: sequência sintaticamente válida.")
    except Exception as e:
        print(f"Erro de análise sintática: {e}")

if __name__ == "__main__":
    main()