import configuracoes


class Test_Configuracoes_Converte_txt_para_lista:
    def test_converte_txt_para_lista_1(self):
        result = configuracoes.converte_txt_para_lista("path/to/file.ext")

    def test_converte_txt_para_lista_2(self):
        result = configuracoes.converte_txt_para_lista("/path/to/file")

    def test_converte_txt_para_lista_3(self):
        result = configuracoes.converte_txt_para_lista("./path/to/file")

    def test_converte_txt_para_lista_4(self):
        result = configuracoes.converte_txt_para_lista(".")

    def test_converte_txt_para_lista_5(self):
        result = configuracoes.converte_txt_para_lista(
            "C:\\\\path\\to\\folder\\")

    def test_converte_txt_para_lista_6(self):
        result = configuracoes.converte_txt_para_lista("")
