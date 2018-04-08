from flask import Flask, render_template, request, redirect, session, flash, url_for

from jogo import Jogo
from usuario import Usuario

app = Flask(__name__)
app.secret_key = "secret_jogoteca"

titulo = "Jogos"
jogo1 = Jogo("Super Mario", "Ação", "SNES")
jogo2 = Jogo("Pokemon Gold", "Aventura", "GBA")
jogo3 = Jogo("Mostal Kombate", "Luta", "SNES")
lista = [jogo1, jogo2, jogo3]

usuario1 = Usuario('luan', 'Luiz Antonio Marques', '1234')
usuario2 = Usuario('Nico', 'Nico Steppat', '7a1')
usuario3 = Usuario('flavio', 'flavio Almeida', 'javascript')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2,
            usuario3.id: usuario3}

@app.route("/")
def index():
    return render_template("lista.html", titulo=titulo, jogos=lista)

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
    lista.append(Jogo(nome, categoria, console))
    return redirect(url_for('index'))

@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)

@app.route("/autenticar", methods=["POST", ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
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

app.run(debug=True, host="localhost", port=8080)