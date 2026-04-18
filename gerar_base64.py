import base64


def converter_audio_para_base64(caminho_arquivo: str) -> str:
    """
    Lê um arquivo binário e retorna sua representação em formato de string Base64.
    """
    with open(caminho_arquivo, "rb") as arquivo:
        conteudo_binario = arquivo.read()
        string_base64 = base64.b64encode(conteudo_binario).decode('utf-8')
        return string_base64


if __name__ == "__main__":
    caminho_do_seu_audio = "audio_tests/dev_test_01.mp3"

    try:
        resultado_base64 = converter_audio_para_base64(caminho_do_seu_audio)

        with open("audio_tests/saida_base64.txt", "w") as arquivo_saida:
            arquivo_saida.write(resultado_base64)

        print("Conversão concluída! O código Base64 foi salvo em 'saida_base64.txt'.")
    except FileNotFoundError:
        print(f"O arquivo {caminho_do_seu_audio} não foi encontrado.")