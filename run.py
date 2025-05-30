from app import app, db # Importe 'app' e 'db' do seu __init__.py

# ... (outros imports e configurações, se houver) ...

if __name__ == '__main__':
    with app.app_context(): # Garante que estamos no contexto da aplicação
        print("Verificando e criando tabelas no banco de dados...")
        db.create_all() # Este é o comando que cria as tabelas
        print("Tabelas verificadas/criadas.")

    app.run(debug=True) # Sua aplicação Flask vai iniciar aqui