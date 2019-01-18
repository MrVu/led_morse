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
	for key, value in tap_code_ls.items():
		for n in range(0, len(word_ls)):
			if word_ls[n] == value:
				current_word = current_word + key
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
		time_subtract= times[n+1]-times[n]
		if time_subtract > 0.5:
			time_index =  times.index(times[n+1])
			tmp_lst.append(time_index)
	return tmp_lst



def index_handling(index_lst, word_ls):
	for n in range(0, len(index_lst), 2):
		try:
			word_ls.append([index_lst[n + 1] - index_lst[n],index_lst[n + 2] - index_lst[n + 1]])
		except Exception as e:
			print(e)
	word_to_send={'word': word_ls, 'received': []}
	return word_to_send



@app.route('/api_1_0/senddata', methods=['POST'])
def send_data():
	if not request.data:
		print('this is the request -------')
		print(request)
		abort(400)
	print(request.data)
        raw_data = request.data
        raw_data_lst= raw_data.split('-')
        print raw_data_lst

	try:
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

