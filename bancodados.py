import mysql.connector


class Banco_de_Dados:
    
    def __init__(self,name=str):
        
        # Conectando ao servidor MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="GameBD",
            auth_plugin='mysql_native_password'  # Adicionando o parâmetro auth_plugin
        )

        # Criando um cursor para executar consultas SQL
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self
        
    
    
    def __exit__(self, exc_type, exc_value, traceback):
        # Fechando a conexão com o banco de dados
        self.conn.close()

        
    def show_tabels(self):
        # Exemplo de consulta SQL
        query = "show Tables;"
        self.cursor.execute(query)
        # Obtendo os resultados
        result = self.cursor.fetchall()
        return result

    def remover_jogador(self, idplayer):
        query = "DELETE FROM posicao WHERE player_idplayer = %s"
        self.cursor.execute(query, (idplayer,))
        self.conn.commit()
        query = "DELETE FROM player WHERE idplayer = %s"
        self.cursor.execute(query, (idplayer,))
        self.conn.commit()

    def visualizar_jogador(self, idplayer):
        queryPlayer = "SELECT * FROM player, posicao WHERE player_idplayer = %s and player_idplayer = %s"
        self.cursor.execute(queryPlayer, (idplayer,idplayer))
        jogador = self.cursor.fetchone()
        if jogador:
            jogador_dict = {
                "idplayer": jogador[0],
                "name": jogador[1],
                "vida": jogador[2],
                "dano": jogador[3],
                "Class": jogador[4],
                "Salve": jogador[5],
                "mapa": jogador[6],
                "x": jogador[7],
                "y": jogador[8]
            }
            return jogador_dict
        else:
            return None

    def visualizar_jogadores(self):
        queryPlayer = "SELECT * FROM player, posicao where idplayer = player_idplayer"
        self.cursor.execute(queryPlayer)
        jogadores = self.cursor.fetchall()
        if jogadores:
            jogares_dicts = []
            print(jogadores)
            for jogador in jogadores:
                jogador_dict = {
                    "idplayer": jogador[0],
                    "name": jogador[1],
                    "vida": jogador[2],
                    "dano": jogador[3],
                    "Class": jogador[4],
                    "Salve": jogador[5],
                    "mapa": jogador[6],
                    "x": jogador[7],
                    "y": jogador[8]
                }
                jogares_dicts.append(jogador_dict)
                
            
            return jogares_dicts
        else:
            return None
    def upadate_player(self,dicionario):
        dicionario['Salve'] = 1
        query = "UPDATE player SET vida = %s, dano = %s,salve = %s WHERE idplayer = %s"
        self.cursor.execute(query, (dicionario['vida'], dicionario['dano'], dicionario['Salve'],dicionario['idplayer']))
        # Commit (confirmar) a transação
        self.conn.commit()
        query = "UPDATE posicao SET mapa = %s, x = %s, y = %s WHERE player_idplayer = %s"
        self.cursor.execute(query, (dicionario['mapa'], dicionario['x'], dicionario['y'],dicionario['idplayer']))
        # Commit (confirmar) a transação
        self.conn.commit()
        
    def adicionar_jogador(self, idplayer, name, vida, dano, Class,salve = 0,maps='m01',x=0,y=0):
        queryPlayer = "INSERT INTO player (idplayer, name, vida, dano, Class, salve) VALUES (%s, %s, %s, %s, %s,%s)"
        self.cursor.execute(queryPlayer, (idplayer, name, vida, dano, Class, salve))
        self.conn.commit()
        queryPos = "INSERT INTO posicao (mapa, x, y, player_idplayer) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(queryPos, (maps, x, y, idplayer))  # Correção aqui
        self.conn.commit()


"""
if __name__ == "__main__":
    banco = Banco_de_Dados()
    # Adicionando um jogador
    banco.remover_jogador(idplayer=1)
    banco.remover_jogador(idplayer=2)

    banco.adicionar_jogador(idplayer=1, name="Jogador1", vida=100, dano=10, Class=1)
    banco.adicionar_jogador(idplayer=2, name="Jogador2", vida=100, dano=10, Class=1)
    print(banco.visualizar_jogadores())
    # Removendo um jogador
    banco.remover_jogador(idplayer=1)
    banco.remover_jogador(idplayer=2)

    # Fechando a conexão com o banco de dados
    del banco    

"""