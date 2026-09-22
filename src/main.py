import sys
from pathlib import Path


SETORES = {
    "SEMS",
    "SEDUC",
    "SEMOSP",
    "SEFIN",
    "SARH",
    "SECOM",
    "SEDEC",
    "SEMAP",
    "SEMOB",
    "SESP",
    "SEMCI",
    "SEDESO",
    "SEGOV",
    "PGM",
    "SEMMADA",
    "SEPLAN",
    "SESMT",
    "SELTC",
}

def listar_arquivos(pasta):
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

def identificar_setor(nome_arquivo):
    nome = nome_arquivo.upper()

    for setor in SETORES:
        if setor in nome:
            return setor

    return None

def verificar_arquivos(pasta):
    corretos = 0
    incorretos = 0
    sem_setor = 0

    for pasta_setor in pasta.iterdir():
        if not pasta_setor.is_dir():
            continue

        setor_pasta = pasta_setor.name.upper()

        # Ignora pastas que não são setores
        if setor_pasta not in SETORES:
            continue

        for arquivo in pasta_setor.iterdir():
            if not arquivo.is_file():
                continue

            setor_arquivo = identificar_setor(arquivo.name)

            if setor_arquivo is None:
                print(f"[SEM SETOR] {pasta_setor.name} -> {arquivo.name}")
                sem_setor += 1

            elif setor_arquivo != setor_pasta:
                print(
                    f"[INCORRETO] {arquivo.name} "
                    f"| Pasta: {setor_pasta} "
                    f"| Identificado: {setor_arquivo}"
                )
                incorretos += 1

            else:
                corretos += 1

    print()
    print(f"Arquivos corretos: {corretos}")
    print(f"Arquivos incorretos: {incorretos}")
    print(f"Arquivos sem setor identificado: {sem_setor}")

def organizar_arquivos(pasta):
    arquivos = [
        arquivo
        for arquivo in pasta.iterdir()
        if arquivo.is_file()
    ]

    organizados = 0
    sem_setor = 0

    for arquivo in arquivos:
        setor = identificar_setor(arquivo.name)

        if setor is None:
            print(f"Setor não identificado: {arquivo.name}")
            sem_setor += 1
            continue

        pasta_setor = pasta / setor
        pasta_setor.mkdir(exist_ok=True)

        destino = pasta_setor / arquivo.name

        arquivo.rename(destino)

        print(f"{arquivo.name} -> {setor}")
        organizados += 1

    print()
    print(f"Concluído: {organizados} arquivos organizados.")

    if sem_setor:
        print(f"Arquivos sem setor identificado: {sem_setor}")    

def main():
    if len(sys.argv) != 3:
        print("Uso:")
        print("  python src/main.py <pasta> listar")
        print("  python src/main.py <pasta> organizar")
        print("  python src/main.py <pasta> verificar")
        sys.exit(1)

    pasta = Path(sys.argv[1])
    modo = sys.argv[2].lower()

    if not pasta.exists():
        print(f"Erro: a pasta não existe: {pasta}")
        sys.exit(1)

    if not pasta.is_dir():
        print(f"Erro: o caminho informado não é uma pasta: {pasta}")
        sys.exit(1)

    if modo == "listar":
        listar_arquivos(pasta)

    elif modo == "organizar":
        organizar_arquivos(pasta)

    elif modo == "verificar":
        verificar_arquivos(pasta)

    else:
        print(f"Erro: modo inválido: {modo}")
        print("Use 'listar' ou 'organizar'.")
        sys.exit(1)


if __name__ == "__main__":
    main()