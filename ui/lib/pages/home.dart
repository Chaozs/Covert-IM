import 'package:flutter/material.dart';
import 'package:ui/pages/chatrooms.dart';
import 'dart:math' as math;

class PeakQuadraticCurve extends Curve {
  @override
  double transform(double t) {
    assert(t >= 0.0 && t <= 1.0);
    return -15 * math.pow(t, 2) + 15 * t + 1;
  }
}

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
        duration: const Duration(seconds: 2), vsync: this);
    animation = CurvedAnimation(parent: controller, curve: Curves.easeInCubic);
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
              SizeTransition(
                sizeFactor: animation,
                child: Center(
                  child: Hero(
                    flightShuttleBuilder: (
                      BuildContext flightContext,
                      Animation<double> animation,
                      HeroFlightDirection flightDirection,
                      BuildContext fromHeroContext,
                      BuildContext toHeroContext,
                    ) {
                      final Hero toHero = toHeroContext.widget;
                      return ScaleTransition(
                        scale: animation.drive(
                          Tween<double>(begin: 0.0, end: 1.0).chain(
                            CurveTween(
                              curve: Interval(0.0, 1.0,
                                curve: PeakQuadraticCurve()),
                            ),
                          ),
                        ),
                        child: toHero.child,
                      );
                    },
                    tag: 'sel_port',
                    child: Material(
                      type: MaterialType.transparency,
                      child: Text(
                        noport ? port : 'YOUR PORT: $port',
                        style: TextStyle(
                          fontSize: 50,
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ),
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
              SizeTransition(
                sizeFactor: animation,
                child: Center(
                  child: GestureDetector(
                    onTap: () {
                      _toChatroom(port);
                    },
                    child: Container(
                      width: 110,
                      height: 110,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: <Widget>[
                          Text(
                            'TAP TO CHAT',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          Image.asset(
                            'assets/images/v.png',
                            height: 80,
                          ),
                        ],
                      ),
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