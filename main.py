import datetime
import monthdelta
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

import jsonUtils

dataFile = "exp.json"
fp = FontProperties(fname="C:\Windows\Fonts\msgothic.ttc", size=12)
fp = FontProperties(fname="/mnt/c/Windows/Fonts/msgothic.ttc", size=12)
SHOW_YEARS = 5

def inputLogData():
	""" 実行時点のデータを取得
		Return:
			jdata	jsonデータ
		"""

	while 1:
		bank = input("銀行預金: ")
		if (bank.isdigit()):
			break
	while 1:
		cash = input("財布現金: ")
		if (cash.isdigit()):
			break
	while 1:
		card = input("カード払: ")
		if (card.isdigit()):
			break

	jdata = {"when": datetime.date.today().strftime('%Y-%m-%d'), "bank": int(bank), "cash": int(cash), "card": int(card)}
	return jdata

def inputExpData():
	""" 出費データを取得
		Return:
			jdata	jsonデータ
		"""

	expDate = datetime.date.today()
	expDate = "{}".format(expDate)

	if (input("出費日付は {} ?[Y/n]: ".format(expDate)) == "n"):
		while 1:
			expDate = input("出費日付(yyyy-mm-dd): ")
			try:
				tmpDate = datetime.datetime.strptime(expDate, '%Y-%m-%d')
				break
			except Exception as e:
				continue

	title = input("タイトル: ")

	while 1:
		exp = input("出費額: ")
		if (exp.isdigit()):
			break

	while 1:
		month = input("有効期間(0:期間なし)[ヵ月]: ")
		if (month.isdigit()):
			break

	jdata = {"when": expDate, "title": title, "exp": int(exp), "month": int(month)}
	return jdata

def printGraph():
	""" 履歴をグラフに表示 """

	jdata = jsonUtils.readJsonFile(dataFile)
	if (jdata == {}):
		return 404

	xl = []
	yl = []
	yd = []
	expi = 0
	# 月々のデータを取得
	for row in jdata['log']:
		adj = 0
		if ('adj' in row):
			adj = row['adj']

		when = datetime.datetime.strptime(row['when'], '%Y-%m-%d')
		if (datetime.date(when.year + SHOW_YEARS, when.month, when.day) < datetime.date.today()):
			continue

		xl.append(when)
		yl.append(row['bank'] + row['cash'] - row['card'])

		# 定期出費を計上
		dum = 0
		for erow in jdata['exp']:
			ewhen = datetime.datetime.strptime(erow['when'], '%Y-%m-%d')
			ewhen = ewhen.date() - datetime.timedelta(days=ewhen.day - 1)
			ldate = when.date() - datetime.timedelta(days=when.day - 1)

			if ((ldate > ewhen) and (ldate <= ewhen + monthdelta.monthdelta(erow['month']))):
				dum += erow['exp'] * (monthdelta.monthmod(ldate, ewhen + monthdelta.monthdelta(erow['month']))[0].months) / erow['month']

		yd.append(row['bank'] + row['cash'] - row['card'] + adj + dum)

	xe = []
	ye = []
	for row in [row for row in jdata['exp'] if row['month'] == 0]:
		when = datetime.datetime.strptime(row['when'], '%Y-%m-%d')
		if (datetime.date(when.year + SHOW_YEARS, when.month, when.day) < datetime.date.today()):
			continue
		xe.append(when)
		ye.append(row['exp'])

	plt.switch_backend("agg")
	plt.subplots(figsize=(16, 9))
	plt.plot(xl, yd, label="dummy", linestyle="--")
	plt.plot(xl, yl, label="log")
	plt.scatter(xe, ye, label="expense", color="red")
	plt.xlabel("when")
	plt.ylabel("金額", fontproperties=fp)
	plt.legend()

	plt.savefig("log.png")

	return 0

if __name__ == '__main__':
	""" main """

	# データ取得
	jdata = jsonUtils.readJsonFile(dataFile)
	if (jdata == {}):
		jdata = {"log": [], "exp": []}

	if (input("ログデータを入力?[Y/n]: ") != "n"):
		ldata = inputLogData()
		jdata['log'].append(ldata)

	if (input("出費データを入力?[Y/n]: ") != "n"):
		edata = inputExpData()
		jdata['exp'].append(edata)

	# データ書込
	jdata['exp'].sort(key=lambda x: x['when'])
	jsonUtils.writeJsonFile(dataFile, jdata)

	# グラフ作成
	printGraph()

	print("return 0")
