'''
Based off of Harry Browne's permanent portfolio
The portfolio aims for the following allocation:
	Total Stock Market: 25%
	Long Term Treasuries: 25%
	Gold: 25%
	Cash: 25%

We are using the following mappings:
	Total Stock Market: VTI
	Long Term Treasuries: VGLT
	Gold: GLD
	Cash: (settlement fund)

This program is cash-biased. This is evident especially when working with small numbers.
'''


import math
import pandas
from alpha_vantage.timeseries import TimeSeries

api_key = '8FIYTT49ZEZT2GV5'
ts = TimeSeries(key=api_key, output_format='pandas')

accountValue = float(input('\nWhat is the current value of the account? '))
action = float(input('Do you want to REBALANCE (0) or ADD (1) to or REMOVE (2) from the account? '))
if action == 1:
	CASHchange = float(input('How much do you want to add to the account? '))
elif action == 2:
	CASHchange = float(input('How much do you want to remove from the account? ')) * -1
elif action == 0:
	CASHchange = 0.0
else:
	print('INVALID INPUT, defaulting to REBALANCE')
	CASHchange = 0.0

VTIshares = float(input('How many shares of VTI do you currently own? '))
VGLTshares = float(input('How many shares of VGLT do you currently own? '))
GLDshares = float(input('How many shares of GLD do you currently own? '))


VTIprice = ((ts.get_intraday(symbol='VTI', interval = '1min', outputsize = 'full')[0])['4. close'])[0]
VGLTprice = ((ts.get_intraday(symbol='VGLT', interval ='1min', outputsize = 'full')[0])['4. close'])[0]
GLDprice = ((ts.get_intraday(symbol= 'GLD', interval='1min', outputsize = 'full')[0])['4. close'])[0]

VTIvalue = VTIprice * VTIshares
VGLTvalue = VGLTprice * VGLTshares
GLDvalue = GLDprice * GLDshares
CASHvalue = accountValue - (VTIvalue + VGLTvalue + GLDvalue) 

print('\n----------STARTING ALLOCATION----------')
print('Cash: $' + str(round(CASHvalue, 2)) + ', ' + str(round((CASHvalue / accountValue) * 100, 1)) + '%')
print('Stocks: $' + str(VTIvalue) + ', ' + str(round((VTIvalue / accountValue) * 100, 1)) + '%')
print('Bonds: $' + str(VGLTvalue) + ', ' + str(round((VGLTvalue / accountValue) * 100, 1)) + '%')
print('Gold: $' + str(GLDvalue) + ', ' + str(round((GLDvalue / accountValue) * 100, 1)) + '%')
print('TOTAL: $' + str(CASHvalue + VTIvalue + VGLTvalue + GLDvalue))

idealCategoryValue = (accountValue + CASHchange) * .25
VTIchange = math.floor((idealCategoryValue - VTIvalue) / VTIprice)
VGLTchange = math.floor((idealCategoryValue - VGLTvalue) / VGLTprice)
GLDchange = math.floor((idealCategoryValue - GLDvalue) / GLDprice)

print('\n----------NEW ORDER----------')
if VTIchange > 0:
	print('VTI: buy ' + str(VTIchange) + ' shares.')
elif VTIchange < 0:
	print('VTI: sell ' + str(VTIchange * -1) + ' shares.')
else:
	print('VTI: do nothing.')

if VGLTchange > 0:
	print('VGLT: buy ' + str(VGLTchange) + ' shares.')
elif VGLTchange < 0:
	print('VGLT: sell ' + str(VGLTchange * -1) + ' shares.')
else:
	print('VGLT: do nothing.')

if GLDchange > 0:
	print('GLD: buy ' + str(GLDchange) + ' shares.')
elif GLDchange < 0:
	print('GLD: sell ' + str(GLDchange * -1) + ' shares.')
else:
	print('GLD: do nothing.')

CASHvalue = CASHvalue + CASHchange - (VTIchange * VTIprice) - (VGLTchange * VGLTprice) - (GLDchange * GLDprice)
VTIvalue = VTIvalue + (VTIchange * VTIprice)
VGLTvalue = VGLTvalue + (VGLTchange * VGLTprice)
GLDvalue = GLDvalue + (GLDchange * GLDprice)
accountValue = CASHvalue + VTIvalue + VGLTvalue + GLDvalue

print('\n-----------NEW ALLOCATION----------')
print('Cash: $' + str(round(CASHvalue, 2)) + ', ' + str(round((CASHvalue / accountValue) * 100, 1)) + '%')
print('Stocks: $' + str(VTIvalue) + ', ' + str(round((VTIvalue / accountValue) * 100, 1)) + '%')
print('Bonds: $' + str(VGLTvalue) + ', ' + str(round((VGLTvalue / accountValue) * 100, 1)) + '%')
print('Gold: $' + str(GLDvalue) + ', ' + str(round((GLDvalue / accountValue) * 100, 1)) + '%')
print('TOTAL: $' + str(CASHvalue + VTIvalue + VGLTvalue + GLDvalue))
print('\n')