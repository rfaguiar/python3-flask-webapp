import time
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from dao.jogoDao import JogoDao
from dao.usuarioDao import UsuarioDao
from model.jogo import Jogo
from helpers import deleta_arquivo, recupera_imagem
from jogoteca import db, app

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

@app.route("/")
def index():
    lista = jogo_dao.listar()
    return render_template("lista.html", titulo="Jogos", jogos=lista)

@app.route("/novo")
def novo():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect("/login?proxima=novo")
    return render_template("novo.html", titulo="Novo jogo")

@app.route("/criar", methods=["POST",])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    jogo = jogo_dao.salvar(Jogo(nome, categoria, console))
    arquivo = request.files["arquivo"]
    upload_path = app.config["UPLOAD_PATH"]
    timestamp = time.time()
    arquivo.save("{}/capa{}-{}.jpg".format(upload_path, jogo.id, timestamp))
    return redirect(url_for('index'))

@app.route("/editar/<int:id>")
def editar(id):
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect("/login?proxima=editar")
    jogo = jogo_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=nome_imagem or 'capa_padrao.jpg')

@app.route("/atualizar", methods=["POST",])
def atualizar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    id = request.form["id"]
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(id)
    arquivo.save('{}/capa{}-{}.jpg'.format(upload_path, id, timestamp))
    jogo_dao.salvar(Jogo(nome, categoria, console, id))
    return redirect(url_for('index'))

@app.route("/excluir/<int:id>")
def excluir(id):
    jogo_dao.deletar(id)
    flash("O jogo foi removido com sucesso!")
    return redirect(url_for("index"))

@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)

@app.route("/autenticar", methods=["POST", ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('login'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)