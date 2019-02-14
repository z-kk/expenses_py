import os
import json

fName = "hoge.json"

def readJsonFile(fileName):
	""" JSONファイルからdictionaryを生成
	params:
		fileName	JSONファイル名
	return:
		dict	JSONデータ
	"""

	if (os.path.exists(fileName)):
		with open(fileName, 'r') as f:
			jdata = json.load(f)
	else:
		jdata = dict()

	return jdata

def writeJsonFile(fileName, jdata):
	""" JSONファイルにdictionaryの内容を書き込む
	params:
		fileName	JSONファイル名
		jdata	dictionaryデータ
	return:
		int		0:書き込み成功
	"""

	try:
		with open(fileName, 'w') as f:
			json.dump(jdata, f, ensure_ascii=False, indent=4, separators=(',', ': '))
	except Exception as e:
		print(e)
		return 1

	return 0

if __name__ == '__main__':
	""" main """

	jdata = readJsonFile(fName)
	if (jdata == {}):
		jdata = {"data": []}

	jdata['data'].append({"hoge": "hoge", "値": 100})

	print(jdata)

	writeJsonFile(fName, jdata)
