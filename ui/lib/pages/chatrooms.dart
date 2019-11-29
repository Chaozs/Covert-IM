import 'package:flutter/material.dart';
import 'package:ui/pages/chatpage.dart';

class ChatroomsPage extends StatelessWidget {
  final List<String> chatrooms = [
     "Normal",
     "TCP",
     "IP",
  ];
  final String port;
  ChatroomsPage({@required this.port});

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
          // leading: Icon(icons[idx]),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => ChatPage(
                  covert: chatrooms[idx], 
                  port: port,)
              )
            );
          },
        ),
      )
    ),
  );
}