import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

const List<IconData> icons = [Icons.ac_unit, 
    Icons.shopping_cart, 
    Icons.wb_sunny,
    Icons.fingerprint,
    Icons.filter_drama
    ];
const IconData me = Icons.adb;
final double myID = Random().nextDouble();
void main() => runApp(CovertUI());

class CovertUI extends StatelessWidget {
  final List<String> chatrooms = [
     "Normal",
     "TCP",
     "IP",
  ];
  @override
  Widget build(BuildContext context) => MaterialApp(
    theme: ThemeData(
      primarySwatch: Colors.green,
      iconTheme: IconThemeData(color: Colors.red),      
    ),
    title: 'Covert Telecommunications',
    home: ChatroomsPage(chatrooms: chatrooms),
  );
}

class ChatWidget extends StatefulWidget {
  final String name;
  final IconData icon;
  ChatWidget({Key key, @required this.name, @required this.icon}) : super(key: key);

  @override
  createState() => _ChatWidgetState();
}

class _Post {
  final String body;

  _Post({this.body});

  factory _Post.fromJson(Map<String, dynamic> json) {
    return _Post(
      body: json['body'],
    );
  }
}

class _ChatWidgetState extends State<ChatWidget> {

  List<String> msgs = [];
  List<bool> sends = [];
  final TextEditingController eCtrl = TextEditingController();

  Future<_Post> _fetchPost(covert, uid) async {
    final response =
        await http.post('http://localhost:5000/chat/get',
        headers: {"Content-Type": "application/json"},
        body: json.encode({'covert': covert, 'uid': uid,}));

    if (response.statusCode == 200) {
      // If the call to the servers was successful, parse the JSON.
      return _Post.fromJson(json.decode(response.body));
    } else {
      // If that call was not successful, throw an error.
      throw Exception('Failed to load post');
    }
  }

  void _pushPost(covert, uid, msg) async {
    final response =
        await http.post('http://localhost:5000/chat/post',
        headers: {"Content-Type": "application/json"},
        body: json.encode({'covert': covert, 'uid': uid, 'msg': msg}));

    if (response.statusCode != 201) {
      throw Exception('Failed to push post');
    }
  }

  // Mock Listen
  final oneSec = Duration(seconds:3);
  @override
  void initState() {
    super.initState();
    Timer.periodic(oneSec, (timer) {
      setState(() {
        _fetchPost(widget.name, myID).then( (data) {
          if(data.body != ''){
              msgs.add('From ${widget.name}: ${data.body}');
              sends.add(false);
            }
          }, onError: (err) {
            print(err);
          });
      });
    });
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: Text(widget.name),
    ),
    floatingActionButtonLocation: FloatingActionButtonLocation.endFloat,
    body: Column(
      children: <Widget>[
        Expanded(
          child: ListView.builder(
            itemCount: msgs.length,
            itemBuilder: (BuildContext context, int idx) => _buildMsg(
              widget.icon, msgs[idx], sends[idx]
            )
          ),
        ),
        Container(
          padding: EdgeInsets.all(10),
          child:TextField(
            controller: eCtrl,
            decoration: InputDecoration(
              border: OutlineInputBorder(),
              icon: Icon(Icons.textsms),
              hintText: 'try to say: Hello',
            ),
            onSubmitted: (input) {
              msgs.add(input);
              sends.add(true);
              eCtrl.clear();
              setState(() { 
                _pushPost(widget.name, myID, input);
                }
              );
            },
          )
        )
      ],
    ),
  );
}

Widget _buildMsg(icon, msg, send) => Container(
  padding: EdgeInsets.only(left: 12),
  child: Row(
    mainAxisAlignment: send ? MainAxisAlignment.end : MainAxisAlignment.start,
    children: <Widget>[
      Icon(
        send ? me : icon,
        // color: Colors.deepPurple[200],
      ),
      Container(
        margin: EdgeInsets.all(10),
        padding: EdgeInsets.all(12),
        alignment: Alignment.center,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.all(
            Radius.circular(5),
          ),
          color: Colors.blue[100]
        ),
        child: Text(
          msg,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w400,
          ),
          softWrap: true,
        ),
      )
    ],
  ),
);

class ChatroomsPage extends StatelessWidget {
  final List<String> chatrooms;
  
  ChatroomsPage({@required this.chatrooms});

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: Text('Hiddenor'),
      // backgroundColor: Colors.deepPurple[200],
    ),
    body: Center(
      child : ListView.builder(
        itemCount: chatrooms.length,
        itemBuilder: (context, idx) => ListTile(
          title: Text(
            chatrooms[idx],
          ),
          leading: Icon(icons[idx]),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => ChatWidget(
                  name: chatrooms[idx], 
                  icon: icons[(idx%5).toInt()])
              )
            );
          },
        ),
      )
    ),
  );
}
