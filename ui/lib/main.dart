import 'package:flutter/material.dart';
import 'package:ui/pages/home.dart';

void main() => runApp(CovertUI());

class CovertUI extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
      primaryColor: Colors.black,
      // iconTheme: IconThemeData(color: Colors.white),      
      ),
      title: 'Covert Telecommunications',
      home: PortPage(),
    );
  }
}
