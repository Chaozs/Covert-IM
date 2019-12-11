import 'package:flutter/material.dart';
import 'package:ui/pages/chatpage.dart';

class ChatroomsPage extends StatelessWidget {
  final List<String> chatrooms = [
     "Normal",
     "IP SPOOF",
     "PORT SPOOF",
  ];
  final String port;
  ChatroomsPage({@required this.port});

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: Text(
        'Covert Channels',
      ),
    ),
    body: SafeArea(
      child : Column(
        children: <Widget>[
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Hero(
              tag: 'sel_port',
              child: Material (
                type: MaterialType.transparency,
                child: Text(
                  'YOUR PORT: $port',
                  style: TextStyle(
                    fontSize: 25,
                        fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: chatrooms.length,
              itemBuilder: (context, idx) => ListTile(
                title: Text(
                  chatrooms[idx],
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                ),
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
            ),
          ),
        ],
      )
    ),
  );
}