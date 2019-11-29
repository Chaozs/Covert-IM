import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:convert';
import 'package:ui/models/post.dart';
import 'package:http/http.dart' as http;
import 'package:ui/widgets/messages.dart';
import 'dart:math';

class ChatPage extends StatefulWidget {
  final String covert;
  final String port;
  final String uid = '${Random().nextDouble()}';
  ChatPage({
    Key key, 
    @required this.covert,
    @required this.port,
    }) : super(key: key);

  @override
  createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final _listKey = GlobalKey<AnimatedListState>();
  List<String> msgs = [];

  final TextEditingController eCtrl = TextEditingController();

  Future<Post> _fetchPost(covert, uid) async {
    final response =
        await http.post('http://localhost:${widget.port}/chat/get',
        headers: {"Content-Type": "application/json"},
        body: json.encode({'covert': covert, 'uid': uid,}));

    if (response.statusCode == 200) {
      // If the call to the servers was successful, parse the JSON.
      return Post.fromJson(json.decode(response.body));
    } else {
      // If that call was not successful, throw an error.
      throw Exception('Failed to load post');
    }
  }

  void _pushPost(covert, uid, msg) async {
    final response =
        await http.post('http://localhost:${widget.port}/chat/post',
        headers: {"Content-Type": "application/json"},
        body: json.encode({'covert': covert, 'uid': uid, 'msg': msg}));

    if (response.statusCode != 201) {
      throw Exception('Failed to push post');
    }
  }

  final oneSec = Duration(seconds:3);
  @override
  void initState() {
    super.initState();
    Timer.periodic(oneSec, (timer) {

        _fetchPost(widget.covert, widget.uid).then( (data) {
          if(data.body != ''){
              msgs.add('${data.body}');
              _listKey.currentState.insertItem(msgs.length-1);
            }
          }, onError: (err) {
            print(err);
          });

    });
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: Text(widget.covert),
    ),
    floatingActionButtonLocation: FloatingActionButtonLocation.endFloat,
    body: Column(
      children: <Widget>[
        Expanded(
          child: AnimatedList(
            key: _listKey,
            initialItemCount: msgs.length,
            itemBuilder: (context, idx, animation) => SizeTransition(
              sizeFactor: animation,
              child: buildMsg(msgs[idx]),)
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
              eCtrl.clear();
              setState(() { 
                _pushPost(widget.covert, widget.uid, input);
                }
              );
            },
          )
        )
      ],
    ),
  );
}