from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests
import simplejson 
import json

app = Flask(__name__, static_folder='../Static', template_folder='../templates')

#Funcoes
def get_rest(link):
    chamar = requests.get(link)
    return chamar.json()

#Paginas
@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", titulo=titulo, css=css, js=js, categorias=categorias, versao=versao)

@app.route("/controle", methods=['GET', 'POST'])
def controle():
    conteudo=""
    listar = request.form.get("listar")
    if listar is not None:
        uri = "https://smi-2020.herokuapp.com/{}/".format(listar)
        expecifico = request.form.get("procurar")
        if expecifico is not None:
            uri = "{}{}".format(uri, expecifico)
        conteudo = get_rest(uri)
    return render_template("controle.html", titulo=titulo, css=css, js=js, categorias=categorias, listar=listar, conteudo=conteudo, versao=versao)


@app.route("/criar", methods=['GET', 'POST'])
def criar():

    listar = request.form.get("listar")
    uri = "https://smi-2020.herokuapp.com/{}/".format(listar)

    if listar == "categorias":
        categoria_add = request.form.get("categoria_add")
        data = {'id':0,'nome':'{}'.format(categoria_add)}

    elif listar == "fornecedores":
        cnpj_add = request.form.get("cnpj_add")    
        nome_cnpj_add = request.form.get("nome_cnpj_add")    
        data = {'cnpj':'{}'.format(cnpj_add), 'id':0, 'nome':'{}'.format(nome_cnpj_add)}

    elif listar == "funcioanarios":
        pass

    elif listar == "produros":
        pass

    elif listar == "setorFuncionarios":
        setorFuncionarios_add = request.form.get("setorFuncionarios_add")
        data = {'id':0,'nome':'{}'.format(setorFuncionarios_add)}
    else:
        pass

    headers = {'Content-type': 'application/json'}
    data_json = json.dumps(data)
    print(data_json)
    requests.post(uri, data=data_json, headers=headers)

    return redirect(url_for("index")) 


@app.route("/atualizar", methods=['GET', 'POST'])
def atualizar():

    listar = request.form.get("listar")
    uri = "https://smi-2020.herokuapp.com/{}/".format(listar)

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
        
    elif listar == "funcioanarios":
        pass

    elif listar == "produros":
        pass

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

    return redirect(url_for("index")) 


#Funcionando
@app.route("/deletar", methods=['GET', 'POST'])
def deletar():

    listar = request.form.get("listar")
    uri = "https://smi-2020.herokuapp.com/{}/".format(listar)
    
    deletar_valor = request.form.get("deletar_valor")

    uri = "{}{}".format(uri, deletar_valor)
    headers = {'Content-type': 'application/json'}

    requests.delete(uri, headers=headers)

    return redirect(url_for("index")) 



#Executar o flask
if __name__ == "__main__":
    titulo = "SMI - Sistema de supermercado inteligente"
    css = ["./Static/css/reset.css", "./Static/css/bootstrap.css", "./Static/css/css_pessoal.css"]
    js = ["./Static/js/jquery-3.4.1.slim.min.js", "./Static/js/bootstrap.js", "./Static/js/popper.min.js", "./Static/js/js_pessoal.js"]
    categorias = ["categorias", "fornecedores", "funcionarios", "produtos", "setorFuncionarios"]
    versao = "0.0.1 - SMI"
    app.run(host='0.0.0.0', debug=True)