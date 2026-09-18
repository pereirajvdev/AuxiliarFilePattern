import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("Uso: python src/main.py <pasta>")
        sys.exit(1)

    pasta = Path(sys.argv[1])

    if not pasta.exists():
        print(f"Erro: a pasta não existe: {pasta}")
        sys.exit(1)

    if not pasta.is_dir():
        print(f"Erro: o caminho informado não é uma pasta: {pasta}")
        sys.exit(1)

    # output fica na raiz do projeto
    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    arquivo_saida = output_dir / "arquivos.txt"

    arquivos = sorted(
        arquivo.name
        for arquivo in pasta.iterdir()
        if arquivo.is_file()
    )

    with arquivo_saida.open("w", encoding="utf-8") as f:
        for nome in arquivos:
            f.write(nome + "\n")

    print(f"Concluído: {len(arquivos)} arquivos encontrados.")
    print(f"Arquivo gerado: {arquivo_saida}")


if __name__ == "__main__":
    main()