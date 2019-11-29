import 'package:flutter/material.dart';

Widget buildMsg(msg) => Padding(
  padding: EdgeInsets.only(left: 12),
  child: Row(
    mainAxisAlignment: MainAxisAlignment.start,
    children: <Widget>[
      Container(
        margin: EdgeInsets.all(7),
        padding: EdgeInsets.all(10),
        alignment: Alignment.center,
        decoration: BoxDecoration(
          color: Colors.black
        ),
        child: Text(
          msg,
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w500,
            color: Colors.white
          ),
          softWrap: true,
        ),
      )
    ],
  ),
);