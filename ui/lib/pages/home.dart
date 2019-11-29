import 'package:flutter/material.dart';
import 'package:ui/pages/chatrooms.dart';

class PortPage extends StatefulWidget {
  @override
  _PortPageState createState() => _PortPageState();
}

class _PortPageState extends State<PortPage> with SingleTickerProviderStateMixin{
  final TextEditingController eCtrl = TextEditingController();
  String port='INPUT YOUR PORT\nTO BEGIN';
  bool noport = true;

  AnimationController controller;
  Animation<double> animation;

  void _handelPort(String text) {
    eCtrl.clear();
    controller.reset();
    setState(() {
      port = '$text';
      noport = false;
    });
    controller.forward();
  }

  void _toChatroom(String port) {
    Navigator.push(context, MaterialPageRoute(
      builder: (context) {
        return ChatroomsPage(port: port,);
      }
    ));
  }

  @override
  initState() {
    super.initState();
    controller = AnimationController(
        duration: const Duration(seconds: 1), vsync: this);
    animation = CurvedAnimation(parent: controller, curve: Curves.easeIn);
    controller.forward();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              FadeTransition(
                opacity: animation,
                child: Text(
                  noport ? port : 'YOUR PORT: $port',
                  style: TextStyle(
                    fontSize: 50,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
              Container(
                padding: EdgeInsets.all(20),
                width: 200,
                child: TextField(
                  controller: eCtrl,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Input your PORT',
                  ),
                  onSubmitted: (text) {
                    _handelPort(text);
                  },
                ),
              ),
              noport? SizedBox() :
              FadeTransition(
                opacity: animation,
                child: GestureDetector(
                  onTap: () {
                    _toChatroom(port);
                  },
                  child: Container(
                    width: 75,
                    height: 110,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: <Widget>[
                        Text(
                          'Tap to Chat'
                        ),
                        Image.asset(
                          'assets/images/v.png',
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}