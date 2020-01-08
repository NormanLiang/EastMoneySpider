# -*- coding: utf-8 -*-

import sys
from enum import Enum

CODE_ONE_SUM = 8000
CODE_TWO_SUM = 3000

MONI_CODE_PRICE = 6.4


class Price_Change(Enum):
	
	ALL_RISE=1
	ALL_FALL=2
	ONE_FALL_TWO_RISE=3
		

def getShiftHand(price_one, price_two, sell_hand):
	hand = (sell_hand*price_one/price_two)/100
	hand = int(hand)*100
	return hand

def getProfit(price_one, price_two, diff, tar, hand, jiage,change):

	price_code_one = {
		Price_Change.ALL_RISE: lambda price_one: price_one+jiage,
		Price_Change.ALL_FALL: lambda price_one: price_one-jiage,
		#Price_Change.ONE_FALL_TWO_RISE: lambda price_one: price_one-jiage,

	}[change](price_one)
	
	price_code_two = price_code_one + diff

	shift_hand = getShiftHand(price_code_two, price_code_one, hand)

#	jieyu = price_code_two*shift_hand - price_code_one*tar

	profit = float(price_code_one*(shift_hand-tar))


	return price_code_one, price_code_two, profit

def getStockSum(origin):
	
	pass


def main(diff_start, diff_end, shift_per=1, jiage=2):

	code_one_price = MONI_CODE_PRICE
	code_two_price = MONI_CODE_PRICE + float(diff_start)

	shift_hand = int(float(shift_per)*CODE_ONE_SUM)

	code_one_last = CODE_ONE_SUM - shift_hand

	shift_hand_last = getShiftHand(code_one_price, code_two_price, shift_hand)

	code_two_last = CODE_TWO_SUM + shift_hand_last

	jieyu = code_one_price*shift_hand - shift_hand_last*code_two_price

	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
	print code_one_last, code_two_last, code_one_price, code_two_price, shift_hand_last, jieyu

	#two price all go up
	price_one_final, price_two_final, profit = getProfit(code_one_price, code_two_price, float(diff_end), shift_hand, shift_hand_last, float(jiage), Price_Change.ALL_RISE)

	jieyu_hou = price_two_final*shift_hand_last - shift_hand*price_one_final

	profit = jieyu + jieyu_hou

	print CODE_ONE_SUM, CODE_TWO_SUM, price_one_final, price_two_final, shift_hand, jieyu_hou
	print 'if base go up, your profit is ', profit
	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
	print code_one_last, code_two_last, code_one_price, code_two_price, shift_hand_last, jieyu

	price_one_final, price_two_final, profit = getProfit(code_one_price, code_two_price, float(diff_end), shift_hand, shift_hand_last, float(jiage), Price_Change.ALL_FALL)

	jieyu_hou = price_two_final*shift_hand_last - shift_hand*price_one_final

	profit = jieyu + jieyu_hou

	print CODE_ONE_SUM, CODE_TWO_SUM, price_one_final, price_two_final, shift_hand, jieyu_hou
	print 'if base go down, your profit is ', profit
	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#	print code_one_last, code_two_last, code_one_price, code_two_price, shift_hand_last, jieyu

#	price_one_final, price_two_final, profit = getProfit(code_one_price, code_two_price, float(diff_end), shift_hand, shift_hand_last, float(jiage), Price_Change.ONE_FALL_TWO_RISE)

#	jieyu_hou = price_two_final*shift_hand_last - code_one_last*price_one_final

#	profit = jieyu + jieyu_hou

#	print CODE_ONE_SUM, CODE_TWO_SUM, price_one_final, price_two_final, shift_hand, jieyu_hou
#	print 'if one down, two up, your profit is ', profit

if __name__ == '__main__':
	if len(sys.argv) == 4:
		main(sys.argv[1], sys.argv[2], sys.argv[3])
	elif len(sys.argv) == 5:
		main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	elif len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])