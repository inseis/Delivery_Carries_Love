import 'package:delivery_service/userPage.dart';
import 'package:flutter/material.dart';
import 'widget/sended_package_info1.dart';


import 'package:firebase_core/firebase_core.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.white,
        child: Center(
          child: Column(
            children: [
              SizedBox(height: 150),
              Container(
                child: Text(
                  '택배는 사랑을 싣고',
                  style: TextStyle(
                    fontWeight: FontWeight.w700,
                    fontSize: 36,
                  ),
                ),
              ),
              Container(
                child: Text(
                  '사랑을 나누는 택배 서비스',
                  style: TextStyle(
                    color: Colors.grey,
                    fontSize: 12,
                  ),
                ),
              ),
              Container(
                margin: EdgeInsets.only(top: 40),
                child:Image.asset(
                  'lib/images/boxwhite.png',
                  width: 250,
                  height: 200,
                ),
              ),
              SizedBox(height: 20),
              Container(
                width: 300,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10),
                  color: Colors.white, // Placeholder color
                ),
                margin: EdgeInsets.only(bottom: 20),
                child: ListTile(
                  title: Text(
                    '택배 보내기',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  subtitle: Text('택배 정보를 입력해 택배를 보냅니다.'),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => SendingPage1()),
                    );
                  },
                ),
              ),
              Container(
                width: 300,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10),
                  color: Colors.white, // Placeholder color
                ),
                child: ListTile(

                  title: Text(
                    '배송 정보 조회',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  subtitle: Text('사용자의 이름을 입력하여 보낸 택배의 정보를 조회할 수 있습니다.'),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => UserDataPage()),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}