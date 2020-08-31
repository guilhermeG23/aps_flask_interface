from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests
import simplejson 
import json

#Flask
app = Flask(__name__, static_folder='../Static', template_folder='../templates')

#Funcoes
def get_rest(link):
    chamar = requests.get(link)
    chamar = chamar.json()
    if type(chamar) is dict:
        chamar = [chamar]
    return chamar

#Paginas
@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", titulo=titulo, css=css, js=js, tabelas=tabelas, versao=versao)

@app.route("/controle", methods=['GET', 'POST'])
def controle():
    conteudo=""
    setores=""
    fornecedor=""
    categorias=""

    if request.args.get("listar") is None:
        listar = request.form.get("listar")
    else:
        listar = request.args.get("listar")

    if listar is not None:
        uri = "{}/{}".format(link_fonte, listar)
        expecifico = request.form.get("procurar")
        if expecifico is not None:
            uri = "{}/{}".format(uri, expecifico)
        conteudo = get_rest(uri)
        #Para listas
        setores = get_rest("{}/setorFuncionarios".format(link_fonte))
        categorias = get_rest("{}/categorias".format(link_fonte))
        fornecedor = get_rest("{}/fornecedores".format(link_fonte))
    return render_template("controle.html", titulo=titulo, css=css, js=js, tabelas=tabelas, listar=listar, conteudo=conteudo, fornecedor=fornecedor, setores=setores, categorias=categorias, versao=versao)

@app.route("/criar", methods=['GET', 'POST'])
def criar():

    listar = request.form.get("listar")
    uri = "{}/{}/".format(link_fonte, listar)

    if listar == "categorias":
        categoria_add = request.form.get("categoria_add")
        data = {'id':0,'nome':'{}'.format(categoria_add)}

    elif listar == "fornecedores":
        cnpj_add = request.form.get("cnpj_add")    
        nome_cnpj_add = request.form.get("nome_cnpj_add")    
        data = {'cnpj':'{}'.format(cnpj_add), 'id':0, 'nome':'{}'.format(nome_cnpj_add)}

    elif listar == "funcionarios":
        nome_add = request.form.get("nome_add")    
        sobrenome_add = request.form.get("sobrenome_add")   
        setores_add = request.form.get("setores_add")   
        usuario_add = "null"
        data = {"id": 0, "nome": "{}".format(nome_add), "setorId": "{}".format(setores_add), "sobreNome": "{}".format(sobrenome_add), "usuarioId": "{}".format(usuario_add)}
    
    elif listar == "lotes":
        #Não funcionando
        entrega_add = request.form.get("entrega_add")    
        valor_add = request.form.get("valor_add")   
        fornecedor_add = request.form.get("fornecedor_add")  
        data = {"dataDeEntrega": "{}".format(entrega_add), "fornecedor": "{}".format(fornecedor_add), "id": 0, "valorCompra": "{}".format(valor_add)}
    
    elif listar == "produtos":
        #Não funcionando
        nome_add = request.form.get("nome_add")    
        marca_add = request.form.get("marca_add")    
        descricao_add = request.form.get("descricao_add")    
        preco_add = request.form.get("preco_add")    
        categoria_add = request.form.get("categoria_add")    
        fornecedor_add = request.form.get("fornecedor_add")    
        data = {"categoria": "{}".format(categoria_add), "descricao": "{}".format(descricao_add), "fornecedores": "{}".format(fornecedor_add), "id": 0, "marca": "{}".format(marca_add), "nome": "{}".format(nome_add), "preco": "{}".format(preco_add)}

    elif listar == "setorFuncionarios":
        setorFuncionarios_add = request.form.get("setorFuncionarios_add")
        data = {'id':0,'nome':'{}'.format(setorFuncionarios_add)}

    else:
        pass

    headers = {'Content-type': 'application/json'}
    data_json = json.dumps(data)
    requests.post(uri, data=data_json, headers=headers)

    return redirect(url_for("controle", listar=listar)) 


@app.route("/atualizar", methods=['GET', 'POST'])
def atualizar():

    listar = request.form.get("listar")
    uri = "{}/{}/".format(link_fonte, listar)

    if listar == "categorias":
        categoria_id_alt = request.form.get("categoria_id_alt")
        categoria_nome_alt = request.form.get("categoria_nome_alt")
        uri=uri + "{}".format(categoria_id_alt)
        data = {'id':'{}'.format(categoria_id_alt),'nome':'{}'.format(categoria_nome_alt)}

    elif listar == "fornecedores":
        fornecedor_id_atl = request.form.get("fornecedor_id_atl")
        fornecedor_cnpj_atl = request.form.get("fornecedor_cnpj_atl")
        fornecedor_nome_atl = request.form.get("fornecedor_nome_atl")
        uri=uri + "{}".format(fornecedor_id_atl)
        data = {'cnpj':'{}'.format(fornecedor_cnpj_atl),'id':'{}'.format(fornecedor_id_atl),'nome':'{}'.format(fornecedor_nome_atl)}

    elif listar == "funcionarios":
        funcionario_id_atl = request.form.get("funcionario_id_atl")
        nome_alt = request.form.get("nome_alt")    
        sobrenome_alt = request.form.get("sobrenome_alt")
        setores_alt = request.form.get("setores_alt")   
        usuario_alt = "1" #Alterar depois
        uri=uri + "{}".format(funcionario_id_atl)
        data = {"id": int('{}'.format(funcionario_id_atl)), "nome": "{}".format(nome_alt), "usuarioId": '{}'.format(usuario_alt), "setor": int("{}".format(setores_alt)), "sobreNome": "{}".format(sobrenome_alt)}

    elif listar == "lotes":
        lote_id_atl = request.form.get("lote_id_atl")
        entrega_alt = request.form.get("entrega_alt")
        valor_alt = request.form.get("valor_alt")
        fornecedor_alt = request.form.get("fornecedor_alt")
        uri=uri + "{}".format(lote_id_atl)
        data = {"dataDeEntrega": "{}".format(entrega_alt), "fornecedor": "{}".format(fornecedor_alt), "id": "{}".format(lote_id_atl),"valorCompra": "{}".format(valor_alt)}

    elif listar == "produros":
        #Nao funciona
        produto_id_atl = request.form.get("produto_id_atl")
        nome_alt = request.form.get("nome_alt")
        marca_alt = request.form.get("marca_alt")
        preco_alt = request.form.get("preco_alt")
        desc_alt = request.form.get("desc_alt")
        fornecedor_alt = request.form.get("fornecedor_alt")
        categoria_alt = "null"
        uri=uri + "{}".format(produto_id_atl)
        data = {"categoria": "{}".format(categoria_alt), "descricao": "{}".format(desc_alt), "fornecedores": "{}".format(fornecedor_alt), "id": "{}".format(produto_id_atl), "marca": "{}".format(marca_alt), "nome": "{}".format(nome_alt), "preco": "{}".format(preco_alt)}

    elif listar == "setorFuncionarios":
        setor_id_alt = request.form.get("setor_id_alt")
        setor_nome_alt = request.form.get("setor_nome_alt")
        uri=uri + "{}".format(setor_id_alt)
        data = {'id':'{}'.format(setor_id_alt),'nome':'{}'.format(setor_nome_alt)}
    else:
        pass


    headers = {'Content-type': 'application/json'}
    data_json = json.dumps(data)
    requests.put(uri, data=data_json, headers=headers)

    return redirect(url_for("controle", listar=listar)) 


#Funcionando
@app.route("/deletar", methods=['GET', 'POST'])
def deletar():

    listar = request.form.get("listar")
    uri = "{}/{}/".format(link_fonte, listar)
    
    deletar_valor = request.form.get("deletar_valor")

    uri = "{}{}".format(uri, deletar_valor)
    headers = {'Content-type': 'application/json'}

    requests.delete(uri, headers=headers)

    return redirect(url_for("controle", listar=listar)) 

#Executar o flask
if __name__ == "__main__":
    titulo = "SMI - Sistema de supermercado inteligente"
    css = ["./Static/css/reset.css", "./Static/css/bootstrap.css", "./Static/css/css_pessoal.css"]
    js = ["./Static/js/jquery-3.4.1.slim.min.js", "./Static/js/bootstrap.js", "./Static/js/popper.min.js", "./Static/js/js_pessoal.js"]
    link_fonte = "https://smi-2020.herokuapp.com"
    tabelas = ["categorias", "fornecedores", "funcionarios", "lotes", "produtos", "setorFuncionarios"]
    versao = "0.0.2 - SMI - Continuando o projeto"
    app.run(host='0.0.0.0', debug=True)