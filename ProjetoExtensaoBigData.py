import pandas as pd
import os

class Doceria:
    def __init__(self):
        self.vendas_file = "vendas.xlsx"
        self.estoque_file = "estoque.xlsx"
        self.fluxo_caixa_file = "fluxo_caixa.xlsx"
        
        # Verifica se os arquivos já existem, se não, cria novos DataFrames
        if not os.path.exists(self.vendas_file):
            self.vendas_df = pd.DataFrame(columns=["Produto", "Quantidade", "Preço Unitário", "Total"])
            self.vendas_df.to_excel(self.vendas_file, index=False)
        else:
            self.vendas_df = pd.read_excel(self.vendas_file)
        
        if not os.path.exists(self.estoque_file):
            self.estoque_df = pd.DataFrame(columns=["Produto", "Quantidade"])
            self.estoque_df.to_excel(self.estoque_file, index=False)
        else:
            self.estoque_df = pd.read_excel(self.estoque_file)
        
        if not os.path.exists(self.fluxo_caixa_file):
            self.fluxo_caixa_df = pd.DataFrame(columns=["Data", "Descrição", "Valor"])
            self.fluxo_caixa_df.to_excel(self.fluxo_caixa_file, index=False)
        else:
            self.fluxo_caixa_df = pd.read_excel(self.fluxo_caixa_file)

    def adicionar_venda(self):
        produto = input("Nome do produto: ")
        quantidade = int(input("Quantidade vendida: "))
        preco_unitario = float(input("Preço unitário: "))
        total = quantidade * preco_unitario
        
        # Atualiza o DataFrame de vendas
        nova_venda = pd.DataFrame([[produto, quantidade, preco_unitario, total]], columns=self.vendas_df.columns)
        self.vendas_df = pd.concat([self.vendas_df, nova_venda], ignore_index=True)
        self.vendas_df.to_excel(self.vendas_file, index=False)
        
        # Atualiza o fluxo de caixa
        nova_entrada = pd.DataFrame([[pd.Timestamp.now(), f"Venda de {produto}", total]], columns=self.fluxo_caixa_df.columns)
        self.fluxo_caixa_df = pd.concat([self.fluxo_caixa_df, nova_entrada], ignore_index=True)
        self.fluxo_caixa_df.to_excel(self.fluxo_caixa_file, index=False)
        
        # Atualiza o estoque
        if produto in self.estoque_df['Produto'].values:
            self.estoque_df.loc[self.estoque_df['Produto'] == produto, 'Quantidade'] -= quantidade
        else:
            print("Produto não encontrado no estoque!")
        self.estoque_df.to_excel(self.estoque_file, index=False)
        
        print(f"Venda de {quantidade} unidades de {produto} registrada com sucesso!")

    def atualizar_estoque(self):
        produto = input("Nome do produto: ")
        quantidade = int(input("Quantidade a adicionar: "))
        
        if produto in self.estoque_df['Produto'].values:
            self.estoque_df.loc[self.estoque_df['Produto'] == produto, 'Quantidade'] += quantidade
        else:
            nova_entrada = pd.DataFrame([[produto, quantidade]], columns=self.estoque_df.columns)
            self.estoque_df = pd.concat([self.estoque_df, nova_entrada], ignore_index=True)
        
        self.estoque_df.to_excel(self.estoque_file, index=False)
        print(f"Estoque de {produto} atualizado com sucesso!")

    def visualizar_fluxo_caixa(self):
        print("\nFluxo de Caixa:")
        print(self.fluxo_caixa_df)

    def executar(self):
        while True:
            print("\n--- Sistema de Controle de Doceria ---")
            print("1. Adicionar Venda")
            print("2. Atualizar Estoque")
            print("3. Visualizar Fluxo de Caixa")
            print("4. Sair")
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                self.adicionar_venda()
            elif opcao == '2':
                self.atualizar_estoque()
            elif opcao == '3':
                self.visualizar_fluxo_caixa()
            elif opcao == '4':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    sistema = Doceria()
    sistema.executar()
