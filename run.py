from Site import create_app, db, io


app = create_app()
app.app_context().push()

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False
    threaded = True


if __name__ == '__main__':
    io.run(app, host="0.0.0.0", port=2000, debug=True)
    #db.drop_all()
    #db.create_all()
