from flask import Flask, jsonify,abort,make_response,url_for,request
import smtplib
import time
Python
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


app = Flask(__name__)




users = []

auctions = []

auctions_info = []



@app.route('/auctions/new_user', methods=['POST'])
def create_user():
    '''
    curl -i -H "Content-Type: application/json" -X POST -d "{\"name\": \"Name\", \"mail\": \"Mail\"}" http://127.0.0.1:5000/auctions/new_user
    '''
    if not request.json or not 'name' or not 'mail' in request.json:
        abort(400)
    if len(users)!=0:
        t=users[-1]['token'] + 1
    else: t=0
    user = {
        'token': t,
        'Name':request.json.get('name'),
        'mail': str(request.json.get('mail'))
    }

    users.append(user)
    return jsonify({'user': user}), 201


@app.route('/auction/filter/<filter>', methods=['GET'])
def get_auctions(filter):
    #input(filter)
    if filter == 'None':
        return jsonify({'auctions': auctions})
    for auction in auctions:
        if auction['activ'] == filter:
            return jsonify({'auctions': auction})
    abort(404)


@app.route('/auction/auction-info/<int:auction_id>', methods=['GET'])
def get_auction(auction_id):
    infos = []
    try:
        for auction_info in auctions_info:
            if auction_info['auction_id'] == auction_id:
                for user in users:
                    if user['token'] == auction_info['token']:
                        name = user['Name']
                info = {
                    name: auction_info['size']
                }
                infos.append(info)
    except: True
    for auction in auctions:
        if auction['auction_id'] == auction_id:
            auction_info={
                'auction_name':auction['name'],
                "appellation":auction["appellation"],
                'name_creator': auction['name_creator'],
                'mail_creator': auction['mail'],
                'old_price': auction['old_price'],
                'rate': auction['rate'],
                'time': auction['time'],
                'price': auction['price'],
                'info':infos
            }
            return jsonify({'auctions': auction_info})
    abort(404)



@app.route('/auctions/create', methods=['POST'])
def create_auctions():
    '''
    curl -i -H "Content-Type: application/json" -X POST -d "{\"token\": 2, \"name\": \"title\", \"appellation\": \"bugag\", \"price\": 150, \"rate\": 10, \"time\": \"10:36\"}" http://127.0.0.1:5000/auctions/create
    '''
    #input(request.json['appellation'])
    if not request.json or not 'appellation' in request.json:
        abort(400)
    if len(auctions)!=0:
        t=auctions[-1]['auction_id'] + 1
    else: t=0
    for user in users:
        if user['token'] == request.json.get('token'):
            name=user['Name']
            mail=user['mail']
    auction = {
        'auction_id': t,
        'name':request.json.get('name'),
        'appellation': request.json.get('appellation'),
        'name_creator': name,
        'token_creator': request.json.get('token'),
        'mail': mail,
        'price': request.json.get('price'),
        'old_price': request.json.get('price'),
        'rate': request.json.get('rate'),
        'last_koment_id':0,
        'time': request.json.get('time')
    }

    try:
        subject='New auction'
        for user in users:
            mail='{}'.format(user['mail'])
            to_addr = mail
            from_addr='auction-rest@yandex.ru'
            body_text="Added a new auction: {}. \nYou can participate in the auction.".format(request.json.get('appellation'))
            try:
                send_mail(subject, to_addr, from_addr, body_text)
            except: True
    except Exception as e: print(e)
    auctions.append(auction)
    return jsonify({'auctions': auctions}), 201



@app.route('/auctions/make_bet', methods=['POST'])
def make_bet():
    '''
    curl -i -H "Content-Type: application/json" -X POST -d "{\"token\": 2, \"auction_id\": 2, \"bet size\": 10}" http://127.0.0.1:5000/auctions/make_bet
    '''
    if not request.json or not 'auction_id' in request.json:
        abort(400)
    for auction in auctions:
        if auction['auction_id'] == request.json.get('auction_id'):
            if auction['token_creator'] != request.json.get('token'):
                if int(request.json.get('bet size'))%int(auction['rate'])!=0:
                    abort(400)
                else :
                    auction['price'] = auction['price']+int(request.json.get('bet size'))
                    auction['last_koment_id'] = auction['last_koment_id'] + 1
                    tt= auction['last_koment_id']
                    print(tt)
                    auction_info = {
                        'auction_id': request.json.get('auction_id'),
                        'last_koment_id':tt,
                        'token': request.json.get('token'),
                        'size': int(request.json.get('bet size')),
                        'token_creator': request.json.get('token')
                    }
            else: abort(400)
    auctions_info.append(auction_info)
    try:
        for auction_info in auctions_info:
            if auction_info['auction_id'] == request.json.get('auction_id'):
                for auction in auctions:
                    if auction['auction_id'] == auction_info['auction_id']:
                        body_text = "In the auction you are interested in: {}, made a new bid".format(auction['appellation'])
                subject = 'Changing the auction'
                for user in users:
                    if user['token']==auction_info['token']:
                        mail ='{}'.format(user['mail'])
                        to_addr = mail
                        from_addr = 'auction-rest@yandex.ru'
                        try:
                            send_mail(subject, to_addr, from_addr, body_text)
                        except:True
    except: True
    return get_auction(request.json.get('auction_id'))





def send_mail( subject, to_addr, from_addr, body_text):
    """
    Send an mail
    """
    BODY ="\r\n".join((
        "From: %s" % from_addr,
        "To: %s" % to_addr,
        "Subject: %s" % subject,
        "",
        body_text
    ))

    mailserver = smtplib.SMTP('smtp.yandex.ru', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()  # again
    mailserver.login('auction-rest', 'WergSerg2294')
    mailserver.sendmail(from_addr, to_addr,BODY)
    mailserver.quit()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



@app.route('/auction/winer/<int:auction_id>', methods=['GET'])
def isq(auction_id):
    subject = 'Changing the auction'
    for auction in auctions:
        if auction['auction_id'] == auction_id:
            name_auk = auction['name']
            tek_time=time.strftime("%H:%M", time.localtime())
            for auction_info in auctions_info:
                if auction_info['auction_id'] == auction['auction_id'] and auction_info['last_koment_id'] == auction['last_koment_id'] :
                    token=auction_info['token']
                    print(token)
            for user in users:
                if user['token']==token:
                    mail=user['mail']
                    name=user['Name']
            #if auction['time'] ==k: True
            subject='Winning the auction'
            to_addr= mail
            from_addr = 'auction-rest@yandex.ru'
            body_text='Good afternoon, {}. \nYou are the winner of the auction "{}"'.format(name,name_auk)
            send_mail(subject, to_addr, from_addr, body_text)
            return get_auction(auction_id)

if __name__ == '__main__':
    app.run(debug=True)



