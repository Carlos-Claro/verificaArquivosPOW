# -*- coding: utf-8 -*-
import requests
import datetime
import os
import json

class Images(object):
    
    def __init__(self):
        self.URI = 'http://201.16.246.176:5000/'
        #self.URI = 'http://localhost:5000/'
        #self.cwd = '/home/programacao/Python/repositorio/'
        self.cwd = '/home/pow/www/powsites/'
        self.arquivoVerificador = 'relatorios/verificador.json'
        #self.arquivoVerificador = 'relatorios/' + datetime.datetime.now().strftime('%Y-%m-%d') + '.json'
        self.URL_GET = self.URI + 'imoveis/'
        self.verificaArquivo()
        
    def verificaArquivo(self):
        try:
            with open(self.arquivoVerificador,'r') as json_file:
                self.pastas = json.load(json_file)
        except IOError:
            pastas = os.listdir(self.cwd)
            lista_pastas = []
            for pasta in pastas:
                if os.path.isdir(self.cwd + pasta):
                    lista_pastas.append(pasta)
            with open(self.arquivoVerificador,'w') as arq:
                arq.write(json.dumps(lista_pastas))
            self.verificaArquivo()
    
    def atualizarArquivo(self,pop):
        print('pop')
        print(pop)
        pastas = self.pastas
        pastas.remove(pop)
        os.unlink(self.arquivoVerificador)
        with open(self.arquivoVerificador,'w') as arq:
            arq.write(json.dumps(pastas))
        
    
    def listaArquivos(self, pasta):
        if os.path.isdir(pasta):
            lista_arquivos = os.listdir(pasta)
            if len(lista_arquivos):
                lista_retorno = []
                for arquivo in lista_arquivos:
                    if os.path.isfile(pasta + arquivo):
                        if 'F' is arquivo[0]:
                            lista_retorno.append(arquivo)
                return lista_retorno
            else:
                return False
        else:
            return False
    
    modelos = ['T_','T3_','T5_','TM_','650F_','1150F_', 'destaque_', 'destaque_home_']
    
    def getImovelID(self,id):
        res = requests.get(self.URL_GET + id)
        imovel = res.json()
        if not imovel:
            print('imovel nao existe ' + id)
            return False
        else:
            print('imovel existe ' + id)
            return True
    
    def verificaImovelexiste(self,arquivo):
        partes = arquivo.split('_')
        pega_imovel = self.getImovelID(partes[1])
        return pega_imovel
    
    def deletarArquivos(self,pasta,arquivo):
        os.unlink(pasta + arquivo)
        for modelo in self.modelos:
            if os.path.isfile(pasta + modelo + arquivo):
                os.unlink(pasta + modelo + arquivo)
    
    def main(self):
        if len(self.pastas) > 0 :
            for pasta in self.pastas:
                print(pasta)
                pasta_completa = self.cwd + pasta + '/imo/'
                lista = self.listaArquivos(pasta_completa)
                if lista:
                    for arquivo in lista:
                        existe = self.verificaImovelexiste(arquivo)
                        if not existe:
                            self.deletarArquivos(pasta_completa,arquivo)
                            print(arquivo + ' nao existe')
                self.atualizarArquivo(pasta)
        return True

if __name__ == '__main__':
    Images().main()
