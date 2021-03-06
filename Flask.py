from flask import Flask, jsonify, abort, request, json
from pymongo import MongoClient

client = MongoClient(
	'mongodb://vuhoang17891:Vu1781991=@cluster0-shard-00-00-bknlw.mongodb.net:27017,cluster0-shard-00-01-bknlw.mongodb.net:27017,cluster0-shard-00-02-bknlw.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
)
name = 'ipad'
db = client['mydatabase']

app = Flask(__name__)


def arrayToString(word_ls):
	tap_code_ls= {'a':[1,1], 'b':[1,2],'c':[1,3], 'd':[1,4], 'e':[1,5], 'f':[2,1], 'g':[2,2],'h':[2,3], 'i':[2,4],'j':[2,5], 'l':[3,1], 'm':[3,2], 'n':[3,3], 'o':[3,4], 'p':[3,5], 'q':[4,1],'r':[4,2], 's':[4,3],'t':[4,4], 'u':[4,5], 'v':[5,1],'w':[5,2],'x':[5,3],'y':[5,4],'z':[5,5]}
	current_word=""
	#for key, value in tap_code_ls.items():
	for n in range(0, len(word_ls)):
		if word_ls[n] == [1,3]:
		    current_word = current_word + 'c'
                elif word_ls[n]== [1,1]:
                    current_word = current_word + 'a'
                elif word_ls[n] == [1,4]:
                    current_word = current_word + 'd'
                elif word_ls[n] == [1,2]:
                    current_word = current_word + 'b'
                elif word_ls[n] == [2,1]:
                    current_word = current_word + 'f'
                elif word_ls[n] == [1,5]:
                    current_word = current_word + 'e'
                elif word_ls[n] == [2,2]:
                    current_word = current_word + 'g'
                elif word_ls[n] == [2,3]:
                    current_word = current_word + 'h'
                elif word_ls[n] == [2,4]:
                    current_word = current_word + 'i'
                elif word_ls[n] == [2,5]:
                    current_word = current_word + 'j'
                elif word_ls[n] == [3,1]:
                    current_word = current_word + 'l'
                elif word_ls[n] == [3,2]:
                    current_word = current_word + 'm'
                elif word_ls[n] == [3,3]:
                    current_word = current_word + 'n'
                elif word_ls[n] == [3,4]:
                    current_word = current_word + 'o'
                elif word_ls[n] == [3,5]:
                    current_word = current_word + 'p'
                elif word_ls[n] == [4,1]:
                    current_word = current_word + 'q'
                elif word_ls[n] == [4,2]:
                    current_word = current_word + 'r'
                elif word_ls[n] == [4,4]:
                    current_word = current_word + 't'
                elif word_ls[n] == [4,3]:
                    current_word = current_word + 's'
                elif word_ls[n] == [4,5]:
                    current_word = current_word + 'u'
                elif word_ls[n] == [5,1]:
                    current_word = current_word + 'v'
                elif word_ls[n] == [5,2]:
                    current_word = current_word + 'w'
                elif word_ls[n] == [5,3]:
                    current_word = current_word + 'x'
                elif word_ls[n] == [5,4]:
                    current_word = current_word + 'y'
                elif word_ls[n] == [5,5]:
                    current_word = current_word + 'z'
                else:
                    current_word = current_word + " "
                print(current_word)
	return current_word


@app.route('/api_1_0/getdata/<name>', methods=['GET'])
def get_task(name):
	try:
		data = db.my_buzzer_data.find_one({
			'received': {
				'$nin': [name]
			}
		}, {'_id': False})
	except Exception as e:
		print(e)
	if data is None:
		abort(404)
	if len(name) == 0:
		abort(404)
	return jsonify({'data': data})


@app.route('/api_1_0/getdata/<name>', methods=['POST'])
def update_name(name):
	try:
		data = db.my_buzzer_data.find_one({'received': {'$nin': [name]}})
		if data is None:
			abort(404)
		db.my_buzzer_data.update_one({
			'_id': data['_id']
		}, {'$push': {
			'received': name
		}})
		print('push success')
	except Exception as e:
		data = e
		print(e)
	try:
		data = db.my_buzzer_data.find_one({
			'received': {
				'$nin': [name]
			}
		}, {'_id': False})

		if data is None:
			abort(404)
	except Exception as e:
		data = e
	return jsonify({'data': data})

#Handle data array
def data_handle():
	pass
def timestamp_handling(times):
	tmp_lst=[0]
	print('tmp_lst')
	print(tmp_lst)
	for n in range(0, len(times)):
		if n+1 == len(times):
			tmp_lst.append(n+1) # n+1 is final index
			break
		time_subtract= int(times[n+1])-int(times[n])
		if time_subtract > 500:
			time_index =  times.index(times[n+1])
			tmp_lst.append(time_index)
	return tmp_lst



def index_handling(index_lst, word_ls):
	for n in range(0, len(index_lst), 2):
		try:
			word_ls.append([index_lst[n + 1] - index_lst[n],index_lst[n + 2] - index_lst[n + 1]])
		except Exception as e:
        			print(e)
        for signal in word_ls:
            word_to_send= arrayToString(word_ls)
	return word_to_send



@app.route('/api_1_0/senddata', methods=['POST'])
def send_data():
        word_ls=[]
	if not request.data: #neu khong co data
		abort(400)
	print(request.data)
        raw_data = request.data
        raw_data_lst= raw_data.split('-')
        raw_data_lst= raw_data_lst[:-1]#bo gia tri trong o cuoi list
	try:
                tmp_lst = timestamp_handling(raw_data_lst)
                word_signal = index_handling(tmp_lst, word_ls)
                print(word_signal)
                final_word = {'received':[],'word': word_signal }
                db.my_buzzer_data.insert_one(final_word)
		data='Post successfully'
	except Exception as e:
		print(e)
		data = e
	return jsonify({'data':data})


@app.route('/')
def index():
	return "hello world"


if __name__ == '__main__':
	app.run(debug=False, host='10.140.0.2', port='5000')

