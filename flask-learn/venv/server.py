from flask import Flask, jsonify,abort,make_response,url_for,request
import smtplib
#from flask.ext.httpauth import HTTPBasicAuth


app = Flask(__name__)
#auth = HTTPBasicAuth()



users = [
    {
        'token': 1,
        'mail': 'wwwser181@outlook.com',
        'Name': 'Serg'
    },
    {
        'token': 2,
        'mail': 'wwwser181@outlook.com',
        'Name': 'Ivan'
    }
]


auctions = [
]



# @auth.get_password
# def get_password(username):
#     if username == 'miguel':
#         return 'python'
#     return None
#
# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/auction/filter/<filter>', methods=['GET'])
#@auth.login_required
def get_auctions(filter):
    #input(filter)
    if filter == 'None':
        return jsonify({'auctions': auctions})
    for auction in auctions:
        if auction['activ'] == filter:
            return jsonify({'auctions': auction})
    abort(404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/auctions/create', methods=['POST'])
def create_auctions():
    '''
    curl -i -H "Content-Type: application/json" -X POST -d "{\"token\": 2, \"appellation\": \"bugag\", \"price\": 150, \"rate\": 10, \"time\": \"10:36\"}" http://127.0.0.1:5000/auctions/create
    '''
    #input(request.json['appellation'])
    if not request.json or not 'appellation' in request.json:
        abort(400)
    if len(auctions)!=0:
        t=auctions[-1]['id'] + 1
    else: t=0
    for user in users:
        if user['token'] == request.json.get('token'):
            name=user['Name']
    auction = {
        'auction_id': t,
        'appellation': request.json.get('appellation'),
        'name_creator': name,
        'mail': 'wwwser181@outlook.com',
        'price': request.json.get('price'),
        'rate': request.json.get('rate'),
        'time': request.json.get('time')
    }
    # try:
    #     host='mySMTP.server.com'
    #     subject='test mail'
    #     to_addr='wwwser181@outlook.com'
    #     from_addr='python@mydomain.com'
    #     body_text="Test"
    #     send_mail(host, subject, to_addr, from_addr, body_text)
    # except:
    #     print(1)
    auctions.append(auction)
    return jsonify({'auctions': auctions}), 201


@app.route('/auctions/make_bet', methods=['POST'])
def make_bet():
    '''
    curl -i -H "Content-Type: application/json" -X POST -d "{\"auction_id\": 2, \"bet size\": \"bugag\", \"price\": 150, \"rate\": 10, \"time\": \"10:36\"}" http://127.0.0.1:5000/auctions/make_bet
    '''
    if not request.json or not 'auction_id' in request.json:
        abort(400)



def send_mail(host, subject, to_addr, from_addr, body_text):
    """
    Send an mail
    """
    BODY="\r\n".join((
        "From: %s"%from_addr,
        "To: %s"%to_addr,
        "Subject %s"%subject,
        "",
        body_text
    ))

    server= smtplib.SMTP(host)
    server.sendmail(from_addr,[to_addr],BODY)
    server.quit()

# x=input('x=')
# auctions[0]['activ']=str(x)
# print(auctions[0]['activ'])

if __name__ == '__main__':
    app.run(debug=True)


