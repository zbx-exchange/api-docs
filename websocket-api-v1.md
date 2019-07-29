## Access instructions


### WEBSOCKET API

``
wss://ws.zbx.com/websocket
``


<br/>

### Data compression

All data of Websocket API is compressed by GZIP and then encoded by Base64. encode () and returned by binary mode. Client is required to decode and decompress the binary data after receiving it.

<br/>

### Heart beat news


When the user's Websocket client connects to the ZBX Websocket server, the server sends Ping messages to it periodically (currently set to 5 seconds) with a timestamp.
When the user receives the heartbeat message, he should return the pong message in time and contain the same timestamp in the form of: 

```js
{"ping": 1562979600}

{"pong": 1562979600}
```

When the Websocket server sends Ping messages three times in a row but does not receive any Pong messages back, the server will actively disconnect from the client.

Of course, the user can also actively send a message Ping to the server after connecting to the server. When the server receives the message as ping string, it can actively return a pong string.

<br/>

### Disconnect

The user actively disconnects or sends a message close to the ZBX Websocket server；

<br/>

### Subscribe to Subjects

After a successful connection to the Websocket server is established, the Websocket client should send the following request to subscribe to a specific topic:

```js

{"channel":"ex_single_market","market":{Market},"event":"addChannel"}

{"channel":"ex_group_market","group":{Group},"event":"addChannel"}

{"channel":"ex_last_trade","market":{Market},"since":{Since},"event":"addChannel"}

{"channel":"ex_depth_data","market":{Market},"event":"addChannel"}

{"channel":"ex_chart_update","market":{Market},"since":{Since},"interval":{Interval},"event":"addChannel"}


```


After successful subscription, the Websocket client will receive the full amount of data returned by the corresponding topic.

After that, once the subscribed topic is updated, the Websocket client will receive an update message (push) from the server：

<br/>

### Unsubscribe

The format of unsubscribe is as follows：

```js
{"channel":"ex_single_market","market":{Market},"event":"removeChannel"}

{"channel":"ex_group_market","group":{Group},"event":"removeChannel"}

{"channel":"ex_depth_data","market":{Market},"event":"removeChannel"}

{"channel":"ex_last_trade","market":{Market},"event":"removeChannel"}

{"channel":"ex_chart_update","market":{Market},"interval":{Interval},"event":"removeChannel"}

```


<br/>


**K-line data**

> Subscribe

``
   {"channel":"ex_chart_update","market":{Market},"since":{Since},"interval":{Interval},"event":"addChannel"}
``

> Unsubscribe

``
   {"channel":"ex_chart_update","market":{Market},"interval":{Interval},"event":"removeChannel"}
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
market | string | true | N/A | Trading Markets | btc_usdt, eth_usdt...
interval | string | true | N/A | K-Line Type | 1min,5min,15min,30min,1hour,6hour,1day,7day,30day
since | integer | true | 0 | Time Conditions | 0 or Time Stamps of Necessary Time Nodes, 10 Bit Second Level
> Response data
```js
//[ Time stamp, opening price, maximum price, minimum price, closing price, volume, turnover]
{
    "code":200,
    "data":{
        "market":"eth_usdt",
        "records":[[1562987700,101.0,101.0,101.0,101.0,4.0,404.0]], 
        "channel":"ex_chart_update",
        "interval":"15min",
        "isFull":true,
        "since":1562987700
    },
    "info":"success"
}
```

``
Explanation: After a successful subscription, the user will return a full amount of data filtered according to since, and there is a field in the data that isFull is true as an identifier. After that, once there is an update, the Websocket client will receive incremental messages pushed by the server.

``

<br/>

**Aggregate Market（Ticker）**

> Subscribe

``
   {"channel":"ex_single_market","market":{Market},"event":"addChannel"}
``

> Unsubscribe

``
   {"channel":"ex_single_market","market":{Market},"event":"removeChannel"}
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
market | string | true | N/A | Trading Markets | btc_usdt, eth_usdt...

> Response data
```js
// [Market Name, Market Grouping, Current Price, Increase or Decline, Maximum Price, Minimum Price, Volume，turnover]
{
    "code":200,
    "data":{
        "market":"eth_usdt",
        "records":[["eth_usdt",1,101.00,1.98,101.00,101.00,4.0000,404.000000]],
        "channel":"ex_single_market"
    },
    "info":"success"
}
```

<br/>

**Group Aggregation Market（Tickers)**

> Subscribe

``
   {"channel":"ex_group_market","group":{Group},"event":"addChannel"}
``

> Unsubscribe

``
   {"channel":"ex_group_market","group":{Group},"event":"removeChannel"}
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value	
-|-|-|-|-|-
group | string | false | all | Group type | all or trading area (e.g. usdt) or trading pair (e.g. btc_usdt)

> Response Data
```js
// [Market Name, Market Grouping, Current Price, Increase or Decline, Maximum Price, Minimum Price, Volume,turnover]
{
    "code":200,
    "data":{
        "records":[["eth_usdt",1,103.00,1.9800,103.00,101.00,7.0000,711.000000]],
        "channel":"ex_group_market",
        "group":"usdt"
    },
    "info":"success"
}
```

<br/>

**Market Depth**

> Subscription

``
   {"channel":"ex_depth_data","market":{Market},"event":"addChannel"}
``

> Unsubscribe

``
  {"channel":"ex_depth_data","market":{Market},"event":"removeChannel"}
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Description | Range of Value
-|-|-|-|-|-
market | string | true | N/A | Trading Market | btc_usdt, eth_usdt...

> Response data
```js
{
    "code":200,
    "data":{
        "market":"eth_usdt",
        "depth":"0",
        "last":301.22,
        "asks":[[101.00,2.0000],[102.00,1.0000],[103.00,1.0000]],
        "bids":[[100.00,1.0000],[99.00,1.0000],[98.00,1.0000]],
        "channel":"ex_depth_data",
        "isFull":true
    },
    "info":"success"
}
```
``
   Note: Once the subscription is successful, the user will return the full amount of data once, and there will be an isFull field in the data as an identifier for true. After that, the updates will be returned incrementally. Incremental data each price level is the latest data; if the number of 0 means that the price level has been closed or cancelled.
``

<br/>

**The latest transaction in the market**

> Subscribe

``
   {"channel":"ex_last_trade","market":{Market},"since":0,"event":"addChannel"}
``

> Unsubscribe

``
  {"channel":"ex_last_trade","market":{Market},"event":"removeChannel"}
``

> Request parameters

Parameters | Data Types | Necessity | Default Value | Descriptio | Range of Value
-|-|-|-|-|-
market | string | true | N/A | Trading Markets | btc_usdt, eth_usdt...
since | integer | true | 0 | Time Conditions | Time Stamps of 0 or Necessary Time Nodes, 13-Bit Millisecond Level
> Response data
```js
// [timestamp, transaction price, volume, transaction type, record ID]
{
    "code":200,
    "data":{
        "market":"eth_usdt",
        "records":[[1561697199380,301.22,0.1407,"bid",156169718700197],[1561697198572,301.18,4.0000,"bid",156169718600146],[1561697198302,301.18,0.9883,"ask",156169718400145]],
        "channel":"ex_last_trade",
        "isFull":true
    },
    "info":"success"
}
```
``
	Explanation: Once the subscription is successful, the user will return a full amount of data filtered according to since, and there is an isFull field in the data as an identifier for true. After that, once updated, the Websocket client will receive incremental messages pushed by the server。
``
