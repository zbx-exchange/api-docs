## Access instructions


### REST API

``
https://api.zbx.com
``

Due to high latency and poor stability, it is not recommended to access the ZBX API by proxy.

Request header information should be set to：`Content-Type=application/x-www-form-urlencoded`

<br/>

### Frequency Limitation Rules


Assets are acquired three times per second, individual users are acquired 10 times per second, and a single IP is acquired 1000 times per minute, which is 10 minutes longer than the locked account.

<br/>

### Signature description


API requests are likely to be tampered with in the process of transmission over the Internet. In order to ensure that requests are not changed, private interfaces except public interfaces (basic information, market data) must use your API Key for signature authentication to verify whether parameters or parameter values have changed during transmission. Each API Key requires appropriate privileges to access the corresponding interface. Each newly created API Key needs to be assigned permissions. The types of authority are: read, trade, withdraw money. Before using interfaces, check the permission types of each interface and confirm that your API Key has the corresponding permissions.


A legitimate request consists of the following parts:：

Method Request Address: That is to access the server address, such as `api.zbx.com`，such as `api.zbx.com/trade/api/v1/order`。

API Access Key（accesskey）：Access Key in the API Key you applied for.。

Nonce（nonce）：The time stamp of your application's request, 13 milliseconds, will be used by ZBX to verify the validity of your API request.


Signature (signature)：The value computed by the signature to ensure that the signature is valid and untouched, using ZBX `HmacSHA256`。

<br/>

### Signature step


The specification calculates the request for signature because when HMAC is used for signature computation, the results calculated with different contents will be completely different. So before signature calculation, please normalize the request first. Following is an example of querying a request for details of an order:


`https://api.zbx.com/trade/api/v1/getOrder?accesskey={AccessKey}&market={Market}&nonce={Timestamp}&id={OrderId}&signature={Signature}`

The parameter names are sorted according to the order of ASCII codes, and the parameters are connected by the character "&amp;", for example, the following is the result after sorting：

`accesskey=myAccessKey&id=123&market=btc_usdt&nonce=1562919832183`

Note that the value of nonce is a 13-bit millisecond timestamp

Using Secret Key obtained from the website application, HmacSHA256 signature is performed on the parameter string generated above. For example, the result of signing with the above parameters is as follows:

`97b7b71741ca0aec6e0404a5b1c7cb2a78e7bd6c2a8088dbd84a20129dee4fe7`

Finally, the signature is assigned to the parameter name signature and submitted to the server.

<br/>

### Return Format

All interface returns are in JSON format

<br/>

### Error Code

Status code | Error message
-|:-
101 | Failed to place an order owing to unknown order type
102 | Failed to place an order owing to parameter error
103 | Failed to place an order owing to no sufficient fund
104 | Failed to place an order owing to unknown exception. Please try again later
105 | Failed to place an order, the number of orders must not be lower than the minimum number of orders set by the system
106 | Failed to place an order owing to frequent requests
107 | Failed to place an order since the trade is not open yet
108 | Failed to place an order owing to an incorrect trigger price
109 | Failed to place an order, do not support market order entrustment
110 | Failed to place an order, do not support stop loss order entrustment
111 | Failed to place an order owing to beyond system protection price
121 | Failed to cancel the order since it does not exist or has been canceled
122 | Failed to cancel the order owing to unknown exception. Please try again later
123 | Failed to cancel the order since it has been canceled or completed
124 | Failed to cancel the order owing to frequent requests
404 | Other errors

<br/>

### Market data


**Trading market allocation**

``
    GET /data/api/v1/getMarketConfig
``

> Request parameters


`None`

> Response data

```js
{
  "ltc_usdt": {
    "minAmount": 0.00010,       // Minimum order quantity
    "pricePoint": 2,            // Price decimal point
    "coinPoint": 4,             // Number decimal point
    "maker": 0.00100000,        // Active Single Transaction Fee
    "taker": 0.00100000         // Passive single transaction fee

  }
  "eth_usdt": {
    "minAmount": 0.00010,
    "pricePoint": 2,
    "coinPoint": 4,
    "maker": 0.00100000,
    "taker": 0.00100000
  },
  "btc_usdt": {
    "minAmount": 0.0000010,
    "pricePoint": 2,
    "coinPoint": 6,
    "maker": 0.00100000,
    "taker": 0.00100000
  }
}
```

<br/>

**K-line data**

``
    GET /data/api/v1/getKLine
``

> Request parameters


Parameters | data types | whether they must | default values | descriptions | range of values
-|-|-|-|-|-
market | string | true | N/A | Trading market | btc_usdt, eth_usdt...
type | string | true | N/A | K-line type | 1min,5min,15min,30min,1hour,6hour,1day,7day,30day
since | integer | true | 0 | time condition，control increment | first 0, then since value of response
> Response data

```js
// [Time stamp，opening price，maximum price，minimum price，closing price，volume，turnover]
{
  "datas": [
    [
      1562923200,
      11634.64,  
      11637.22,
      11627.58,
      11631.43,
      1.144578,
      13314.16264138
    ]
  ],
  "since": 1562923200
}
```

<br/>

**Aggregate Market（Ticker）**

``
    GET /data/api/v1/getTicker
``

> Request parameters


Parameters| Data Type | Necessity | Default Value | Description | Range of Value  
-|-|-|-|-|-
market | string | true | N/A | Market | btc_usdt, eth_usdt...

> Response data

```js
{
  "high": 11776.93,
  "moneyVol": 33765013.61761934,    // Volume
  "rate": 1.3900,                   //24 Increases and Decreases
  "low": 11012.17,
  "price": 11609.92,
  "ask": 11618.25,
  "bid": 11604.08,
  "coinVol": 2944.208780            // Volume
}
```

<br/>

**Updated request parameters for all markets Ticker**

``
    GET /data/api/v1/getTickers
``

> response data


`None`

> Response data
```js
{
  "ltc_usdt": {
    "high": 106.99,
    "moneyVol": 1589953.528784,
    "rate": 4.3400,
    "low": 97.51,
    "price": 105.52,
    "ask": 105.61,
    "bid": 105.46,
    "coinVol": 15507.7052
  },
  "btc_usdt": {
    "high": 11776.93,
    "moneyVol": 33765013.61761934,
    "rate": 1.3900,                 
    "low": 11012.17,
    "price": 11609.92,
    "ask": 11618.25,
    "bid": 11604.08,
    "coinVol": 2944.208780
  }
}
```

<br/>

**Market Depth Data**

``
    GET /data/api/v1/getDepth
``

> Request parameters

Parameters | Data Type | Necessity | Default Value | Description | Value Range
-|-|-|-|-|-
market | string | true | N/A | Trading Market | btc_usdt, eth_usdt...

> Response data

```js
{
  "last": 11591.26,     // Latest Transaction Price
  "asks": [
    [
      11594.80,
      0.049472
    ],
    [
      11594.86,
      0.048462
    ]
  ],
  "bids": [
       [
         11590.06,
         0.188749
       ],
       [
         11588.42,
         0.030403
       ]
   ]
}
```

<br/>

**Recent Market Trading Records**

``
    GET /data/api/v1/getTrades
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
market | string | true | N/A | Market | btc_usdt, eth_usdt...

> Response data
```js
// [Time stamp, transaction price, volume, transaction type, record ID]
[
  [
    1562924059762,
    11613.18,
    0.044448,
    "bid",
    156292405956105
  ],
  [
    1562924059006,
    11613.22,
    0.000086,
    "bid",
    156292405956104
  ]
]
```

<br/>
<br/>

### Transaction API

**Get server time (no signature required) request parameters**

``
    GET /trade/api/v1/getServerTime
``

> Response data


`None`

> Response data

```js
{
  "code": 200,
  "data": {
      "serverTime": 1562924059006
  },
  "info": "success"
}
```
<br/>

**Get Spot Account Assets**

``
    GET /trade/api/v1/getBalance
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
nonce | integer | true | N/A | 13-bit milliseconds | 

> Response data
```js
{
  "code": 200,
  "data": {
    "btc": {
      "freeze": "0.00",     // Freeze
      "available": "0.00"   // available
    },
    "eth": {
      "freeze": "0.00",
      "available": "0.00"
    },
    "usdt": {
      "freeze": "3062.17437341",
      "available": "3867.43650012"
    },
    "ltc": {
      "freeze": "0.00",
      "available": "0.00"
    }
  },
  "info": "success"
}
```

<br/>

**Get Account Type (no signature required) request parameters**

``
    GET /trade/api/v1/getAccounts
``

>Request parameters

`None`

>Response data
```js
{
  "code":200,
  "data":[
  	{"name":"钱包账户","enName":"Wallet Account","id":1},
  	{"name":"交易账户","enName":"Spot Account","id":2},
  	{"name":"法币账户","enName":"Fiat Account","id":3}
  ],
  "info":"success"
}
```
``
	Fixed system account type, no real-time access
``

<br/>

**Get Designated Account Assets**

``
    GET /trade/api/v1/getFunds
``

>Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
account | integer | true | N/A | Account ID | Reference to getAccounts interface
nonce | integer | true | N/A | 13-bit milliseconds | 

>Response data
```js
{
  "code": 200,
  "data": {
    "btc": {
      "freeze": "0.00",     // freeze
      "available": "0.00"   // available
    },
    "eth": {
      "freeze": "0.00",
      "available": "0.00"
    },
    "usdt": {
      "freeze": "3062.17437341",
      "available": "3867.43650012"
    },
    "ltc": {
      "freeze": "0.00",
      "available": "0.00"
    }
  },
  "info": "success"
}
```

<br/>

**Transfer of funds between accounts**

``
    POST /trade/api/v1/transfer
``

>Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value 
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
nonce | integer | true | N/A | 13-bit milliseconds | 
from | integer | true | N/A | Account ID | Reference to getAccounts interface
to | integer | true | N/A | Account ID | Reference to getAccounts interface
amount | float | true | N/A | Quantity | 
coin | string | true | N/A | crypto |btc,eth,usdt... 
safePwd | string | true | N/A | Security password | 

>Response data
```js
{
	"code":200,
	"info":"Succeeded"
}
```

<br/>


**Entrust**

``
    POST /trade/api/v1/order
``

> Request parameters


Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
nonce | integer | true | N/A | 13-bit milliseconds | 
market | string | true | N/A | trading market | btc_usdt, eth_usdt...
price | float | true | N/A | Commission price | 
number | float | true | N/A | number of commissions | 
type | integer | true | N/A | type of transaction | 1、buy 0、sell
entrustType | integer | true | N/A | type of commission sale | 0、limit price，1、market price


> Response data

```js
{
  "code": 200,
  "data": {
    "id": 156292794190713
  },
  "info": "An order has been placed successfully"
}
```

<br/>

**Batch commissioning**

``
    POST /trade/api/v1/batchOrder
``

> Request parameters

Parameters | Data Type | Necessity | Default Value | Description | Range of Value 
-|-|-|-|-|-
accesskey | string | true | N/A | Access Key | 
nonce | integer | true | N/A | 13-Bit Millisecond | 
market | string | true | N/A | Market | btc_usdt, eth_usdt...
data | string | true | N/A | Order Data | 

```
Supporting only Price-Limiting delegation, one transaction, either succeeds or fails

Data is a JSON array. The maximum length of the array is only 100, and more than 100 elements will be ignored. The format of the array elements is as follows:

{
  "price": 1000,
  "amount": 1,
  "type" : 1    // 1、buy 0、sell 
}

After assembly, the JSON array is converted to STRING and Base64. Encode () is the final data to be submitted.

Note that data participates in signing not the JSON data itself, but STRING after Base64. Decode ()
```

> Response data
```js
{
  "code": 200,
  "data": [
    {
      "amount": 0.0010,
      "price": 5000.0000,
      "id": 156292972664756,
      "type": 1
    },
    {
      "amount": 0.0020,
      "price": 5000.0000,
      "id": 156292972664757,
      "type": 1
    }
  ],
  "info": "An order has been placed successfully"
}
```

<br/>

**Cancel the order**

``
    POST /trade/api/v1/cancel
``

> Request parameters

Parameters | Data Type | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access Key | 
nonce | integer | true | N/A | 13-Bit Millisecond | 
market | string | true | N/A | Market | btc_usdt, eth_usdt...
id | integer | true | N/A | Order ID |

> Response data
```js
{
  "code": 200,
  "info": "The order has been canceled successfully"
}
```

<br/>

**Batch withdrawal**

``
    POST /trade/api/v1/batchCancel
``

> Request parameters

Parameters | Data Type | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access Key | 
nonce | integer | true | N/A | 13-Bit Millisecond | 
market | string | true | N/A | Market | btc_usdt, eth_usdt...
data | string | true | N/A | Order Data | 

```
Data is a JSON array. The maximum length of the array is only 100, and more than 100 elements are ignored. The array elements are formatted as order ID, such as:

[123, 456, 789]

After assembly, the JSON array is converted to STRING and Base64. Encode () is the final data to be submitted.

Note that data participates in signing not the JSON data itself, but STRING after Base64. Decode ().
```

> Response data
```js
{
  "code": 200,
  "data": [
    {
      "msg": "The order has been canceled successfully",
      "code": 120,
      "id": 156293034776986
    },
    {
      "msg": "The order has been canceled successfully",
      "code": 120,
      "id": 156293034776987
    },
    {
      "msg": "Failed to cancel the order since it does not exist or has been canceled",
      "code": 121,
      "id": 156293034776988
    }
  ],
  "info": "The order has been canceled successfully"
}
```

<br/>

**Order information**

``
    GET /trade/api/v1/getOrder
``

> Request parameters

Parameters | Data Type | Necessity | Default Value | Description | Range of Value,
-|-|-|-|-|-
accesskey | string | true | N/A | Access Key | 
nonce | integer | true | N/A | 13-Bit Millisecond | 
market | string | true | N/A | Market | btc_usdt, eth_usdt...
id | integer | true | N/A | Order ID|

> Response data
```js
{
  "code": 200,
  "data": {
    "number": "0.002000",           // Entrusted quantity
    "price": "5000.00",             // entrusted price
    "avgPrice": "0.00",             // average transaction price
    "id": 156293034776987,          // order ID
    "time": 1562930348000,          // entrusted time
    "type": 1,                      // transaction type: 1, buy 0, sell 
    "status": 3,                    // status  (0、submission uncompleted，1、uncompleted or partial transaction，2、completed，3、cancelled，4、Combined settlement)
    "completeNumber": "0.000000",   // Amount completed
    "completeMoney": "0.000000",    // completed amount
    "entrustType": 0,               // order type：1、market price 0、Price Limitation
    "fee": "0.000000"               // Transaction charges
  },
  "info": "success"
}
```

<br/>

**Getting an unfinished order**

``
    GET /trade/api/v1/getOpenOrders
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
nonce | integer | true | N/A | 13-bit milliseconds | 
market | string | true | N/A | trading market | btc_usdt, eth_usdt...
page | integer | false | 1 | page number | 
pageSize | integer | false | 10 | order number | [10-1000]

> Response data
```js
{
  "code": 200,
  "data": [
    {
      "number": "0.002000",
      "price": "5000.00",
      "avgPrice": "0.00",
      "id": 156293034074105,
      "time": 1562930340271,
      "type": 1,
      "status": 1,
      "completeNumber": "0.000000",
      "completeMoney": "0.000000",
      "entrustType": 0,              
      "fee": "0.000000"
    },
    {
      "number": "0.001000",
      "price": "5000.00",
      "avgPrice": "0.00",
      "id": 156293034074104,
      "time": 1562930340271,
      "type": 1,
      "status": 1,
      "completeNumber": "0.000000",
      "completeMoney": "0.000000",
      "entrustType": 0,              
      "fee": "0.000000"
    }
  ],
  "info": "success"
}
```

<br/>

**Getting multiple order information**

``
    GET /trade/api/v1/getBatchOrders
``

> Request parameters


Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
nonce | integer | true | N/A | 13-bit milliseconds | 
market | string | true | N/A | trading market | btc_usdt, eth_usdt...
data | string | true | N/A | order data | 

```
Data is a JSON array. The maximum length of the array is only 100, and more than 100 elements are ignored. The array elements are formatted as order ID, such as:
[123, 456, 789]

After assembly, the JSON array is converted to STRING and Base64. Encode () is the final data to be submitted.
Note that data participates in signing not the JSON data itself, but STRING after Base64. Decode ()
```

> Response data
```js
{
  "code": 200,
  "data": [
    {
      "number": "0.002000",
      "price": "5000.00",
      "avgPrice": "0.00",
      "id": 156293034074105,
      "time": 1562930340271,
      "type": 1,
      "status": 1,
      "completeNumber": "0.000000",
      "completeMoney": "0.000000",
      "entrustType": 0,              
      "fee": "0.000000"
    },
    {
      "number": "0.001000",
      "price": "5000.00",
      "avgPrice": "0.00",
      "id": 156293034074104,
      "time": 1562930340271,
      "type": 1,
      "status": 1,
      "completeNumber": "0.000000",
      "completeMoney": "0.000000",
      "entrustType": 0,              
      "fee": "0.000000"
    }
  ],
  "info": "success"
}
```

<br/>

**Get the deposit address (In testing)**

``
    GET /trade/api/v1/getPayInAddress
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
nonce | integer | true | N/A | 113-bit milliseconds | 
coin | string | true | N/A | Name of currency | btc,eth,ltc...

> Response data
```js
{
	"code": 200,
	"data": {
		"record": [{
			"chainName": "omni",    // Chain type
			"chain": "btc",         // main chain currency
			"address": "1EAEoYaXx93tKgvrfgpna19GPqC4J2Xcp7",  // recharge address
			"coin": "USDT",         // current currency
			"memo": ""
		}, 
		{
			"chainName": "usdt-erc20",
			"chain": "eth",
			"address": "0x8390b456fe03139ba402f45be9110a5fadf7e862",
			"coin": "USDT",
			"memo": ""
		}]
	},
	"info": " success "
}
```

<br/>

**Get the withdraw address (In testing)**

``
    GET /trade/api/v1/getPayOutAddress
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
nonce | integer | true | N/A | 13-bit milliseconds | 
coin | string | true | N/A | currency name | btc,eth,ltc...
page | integer | true | 1 | paging number | 
pageSize | integer | true | 10 | number of pages per page| 


> Response data

```js
{
	"code": 200,
	"data": {
		"record": [{
			"chainName": "ERC-20",      // Main Chain Name
			"chain": "eth",             // Main Chain Currency
			"address": "0x8390b456fe03139ba402f45be9110a5fadf7e862", // Cash Address
			"memo": "",                 
			"coin": "usdt"              // Current Currency
		}, {
			"chainName": "omni",
			"chain": "btc",
			"address": "1EAEoYaXx93tKgvrfgpna19GPqC4J2Xcp7",
			"memo": "",
			"coin": "usdt"
		}]
	},
	"info": " Success "
}
```

<br/>

**Getting deposit records (In testing)**

``
    GET /trade/api/v1/getPayInRecord
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
nonce | integer | true | N/A | 13-bit milliseconds | 
coin | string | true | N/A | currency name | btc,eth,ltc...
page | integer | true | 1 | paging number | 
pageSize | integer | true | 10 | number of pages per page | 


> response data
```js
{
 	"code": 200,
 	"data": {
 		"total": 1,
 		"pageIndex": 1,
 		"record": [{
 			"chainName": "ERC-20",      // Main Chain Name
 			"amount": 0.001000000,      // Currency Number
 			"chain": "eth",             // Main Chain Currency Number
 			"address": "0x145e96ff8388e474df8c799fb433f103f42d9462",
 			"depth": 12,                // Confirmation Number
 			"creatTime": 1563465915000,
 			"manageTime": 1563466260000,
 			"txHash": "0x4bcd1207e57dc96737d20198c8792c3340386e7f247571458d17671b7834ddd6", // Trading Hash
 			"status": "success",        // Status
 			"coin": "usdt"              // Current Currency
 		}],
 		"pageSize": 100
 	},
 	"info": " Success "
 }
```

<br/>

**Obtain the withdrawal record (In testing)**

``
    GET /trade/api/v1/getPayOutRecord
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
nonce | integer | true | N/A | 13-bit milliseconds | 
coin | string | true | N/A | currency name | btc,eth,ltc...
page | integer | true | 1 | paging number | 
pageSize | integer | true | 10 | number of pages per page | 


> Response data
```js
{
	"code": 200,
	"data": {
		"record": [{
			"chainName": "ERC-20",      // Main Chain Name
			"amount": 0.002000000,      // Number of Currencies
			"chain": "eth",             // Main Chain Currency
			"address": "0x8390b456fe03139ba402f45be9110a5fadf7e862",    // Payment Address
			"creatTime": 1563513678000, // Payment Time
			"fee": 0.001000000,         // Processing Fee
			"manageTime": 1563513698000,// Processing Time
			"status": 4,
			"coin": "usdt"
		}]
	},
	"info": " Success "
}
```

<br/>

**Withdrawal Configuration (In testing)**

``
    GET /trade/api/v1/getWithdrawConfig
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
nonce | integer | true | N/A | 13-bit milliseconds | 


> Response data
```js
{
  "code": 200,
  "data": {
      "btc": {
          "minAmount": 0.01,    // minimum withdrawal amount per time
          "maxAmount": 10,      // daily withdrawal amount
          "fee": 0.0005         // default-handling fee
      },
      "eth": {
          "minAmount": 0.1,
          "maxAmount": 100,
          "fee": 0.005
      }
  },
  "info": "success"
}
```

<br/>

**Withdrawal (In testing)**

``
    GET /trade/api/v1/withdraw
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
accesskey | string | true | N/A | Access key | 
nonce | integer | true | N/A | 13-bit milliseconds | 
coin | string | true | N/A | currency name | btc,eth,ltc...
address | string | true | N/A | withdrawal address | only support your authentication address in ZBX
amount | float | true | N/A | withdrawal number | cannot be lower than the current currency minimum withdrawal security password
safePwd | string | true | N/A | Security Code | 
memo | string | false | Null | note information| 


> Response data
```js
{
  "code": 200,
  "data": {
      
  },
  "info": "success"
}
```

