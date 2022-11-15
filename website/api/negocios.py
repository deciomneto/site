from unicodedata import category
from flask import Blueprint, request, jsonify, url_for
from flask_login import login_required, current_user

from ..mysql import mydb

estab = Blueprint('comercios', __name__)


#--------------------------GET ESTABELECIMENTOS-----------------------------------------------
@estab.route('/api/empresas', methods=['GET'])
def empresa():
    try:
        cursor = mydb.cursor()
        sql = "SELECT * FROM estabelecimentos"
        cursor.execute(sql)
        item = cursor.fetchall()
       
       # print(item)
        itemList = list()
        for items in item:
              itemList.append(
                 {
                    "id": items[0],
                    "nome":items[1],
                    "endereço": items[2],
                    "telefone": items[3],
                    "horário de funcionamento": items[4],
                    "descrição": items[5],
                    "imagem": items[6],
                    "gerente/dono": items[7],
                 
                    
                }
              )
        

            
        return jsonify({
            'mensagem' : 'Lista de Itens',
            'dados': itemList
            
            })
    except Exception as ex:
        return jsonify({'menssagem': "ERRO: dados não existe!"})

   
    
#-------------------------------GET ITEMS ID--------------------------------------------------

@estab.route('/api/empresas/<int:id>', methods=['GET'])
def obter_empresa_por_id(id):
    try:
        cursor = mydb.cursor()

        sql = "SELECT I.id, I.nome, I.endereco, I.telefone, I.hora_func, I.descricao, I.imagem, E.nome FROM estabelecimentos AS I INNER JOIN usuario AS E on E.id = I.user_fk WHERE id = '{0}' ".format(id)
        cursor.execute(sql)
    
        item = cursor.fetchone()
        
        dados = {'id':item[0],'nome':item[1], 'endereço': item[2], 'telefone': item[3], 'horário de funcionamento': item[4], 'descrição': item[5], 'foto': item[6],  'gerente/dono': item[7]}
        return jsonify(dados)
    except Exception as ex:
        return jsonify ({'menssagem': "Erro: registro não encontrado!"})

#-------------------------------POST ITEM--------------------------------------------------
@estab.route('/api/produtos', methods=['POST'])

def incluir_item():
    try:
        item = request.json
        #print(item)
        cursor = mydb.cursor()
        sql ="""INSERT INTO comercios_item (item_id, tipo,nome, marca, quantidade, peso, valor, fim_promo, foto, data, estab_fk) 
        VALUES ({0},'{1}','{2}','{3}','{4}', '{5}','{6}','{7}','{8}','{9}',{10})""".format(item['item'],item['tipo'],item['nome'], item['marca'], item['qtde'], item['peso'], item['valor'],item['fim_promo'], item['foto'], item['data'], item['comercio'])
        
        cursor.execute(sql)
    
        mydb.commit()

        
        return jsonify(
            mensagem="Item cadastrado com sucesso",
        )
    except Exception as ex:
        return jsonify({'menssagem': "Error"})

#--------------------------DELETE ITEMS-----------------------------------------------
@estab.route('/api/produtos/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    try:
        cursor = mydb.cursor()

        sql = "DELETE FROM comercios_item WHERE item_id = '{0}' ".format(id)
        cursor.execute(sql)
    
        mydb.commit()
        
        return jsonify({'menssagem': "Registro deletado com sucesso!"})
    except Exception as ex:
        return jsonify ({'menssagem': "Erro: registro não encontrado!"})

#------------------------UPDATE-----------------------------------------------------
@estab.route('/api/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    try:
        item = request.json
        print(item)
        cursor = mydb.cursor()

        sql = """UPDATE  comercios_item SET tipo='{0}', nome='{1}', marca ='{2}', quantidade ='{3}', peso ='{4}', valor = '{5}', fim_promo = '{6}', foto = '{7}', data = '{8}', estab_fk = {9} 
        WHERE item_id ={10}""".format(item['tipo'], item['nome'], item['marca'], item['qtde'], item['peso'], item['valor'], item['fim promo'], item['foto'], item['comercio'], id)
        
        cursor.execute(sql)
    
        mydb.commit()
        
        return jsonify({'menssagem': "Registro atualizado com sucesso!"})
    except Exception as ex:
        return jsonify ({'menssagem': "Erro: atualização não realizada!"})
#-----------------------------------------------------------------------------------