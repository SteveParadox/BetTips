from Site import create_app, db


app = create_app()
app.app_context().push()

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False
    threaded = True


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
    #db.drop_all()
    #db.create_all()
