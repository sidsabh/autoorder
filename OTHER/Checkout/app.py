from flask import Flask, request, session, render_template


#setup flask app
app = Flask(__name__)
app.config.from_object(__name__)


#Automatically sends user to checkout
@app.route('/checkout/<id>')
def checkout(id):

    return render_template('checkout.html', SESSION_ID=id, PUBLIC_KEY='pk_test_51H7n9PDTJ2YcvBWsgWnXQ3VC2Wh4EbN41ftVHS3hnxLTl2TEZyRUnUcFvpj3B89xsmNEeXJK0PgYhBAezna4iVP800Vrcrphbq')




if __name__ == "__main__":
    app.run(port=8000, debug=True)