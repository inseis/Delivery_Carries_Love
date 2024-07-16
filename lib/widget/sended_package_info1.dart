import 'package:flutter/material.dart';
import 'package:delivery_service/widget/sended_package_info2.dart';

class ControllerFactory {
  static final ControllerFactory _instance = ControllerFactory._internal();

  final Map<String, TextEditingController> _controllers = {};

  factory ControllerFactory() {
    return _instance;
  }

  ControllerFactory._internal();

  TextEditingController getController(String name) {
    if (_controllers[name] == null) {
      _controllers[name] = TextEditingController();
    }
    return _controllers[name]!;
  }

  void disposeAll() {
    _controllers.forEach((key, controller) => controller.dispose());
    _controllers.clear();
  }
}

class SendingPage1 extends StatefulWidget {
  @override
  _SendingPage1State createState() => _SendingPage1State();
}

class _SendingPage1State extends State<SendingPage1> {
  final ControllerFactory _controllerFactory = ControllerFactory();

  bool isButtonEnabled = false;

  @override
  void initState() {
    super.initState();
    _controllerFactory.getController('senderName').addListener(_validateFields);
    _controllerFactory.getController('receiverName').addListener(_validateFields);
    _controllerFactory.getController('senderRegion').addListener(_validateFields);
    _controllerFactory.getController('receiverRegion').addListener(_validateFields);
  }

  @override
  void dispose() {
    _controllerFactory.disposeAll();
    super.dispose();
  }

  void _validateFields() {
    setState(() {
      isButtonEnabled = _controllerFactory.getController('senderName').text.isNotEmpty &&
          _controllerFactory.getController('receiverName').text.isNotEmpty &&
          _controllerFactory.getController('senderRegion').text.isNotEmpty &&
          _controllerFactory.getController('receiverRegion').text.isNotEmpty;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          '이전으로',
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.w600
          ),
        ),
        backgroundColor: Colors.white,
        centerTitle: true,
      ),
      body: Container(
        color: Colors.white, // 배경색을 완전히 흰색으로 설정
        child: SingleChildScrollView(
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 40, vertical: 20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SizedBox(height: 40),
                Text(
                  '택배는 사랑을 싣고',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  '사랑을 나누는 택배 서비스',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.grey,
                  ),
                ),
                SizedBox(height: 40),
                _buildTextField('보낸 사람', 'senderName'),
                SizedBox(height: 20),
                _buildTextField('받는 사람', 'receiverName'),
                SizedBox(height: 60),
                _buildTextField('보내는 지역', 'senderRegion'),
                SizedBox(height: 20),
                _buildTextField('받는 지역', 'receiverRegion'),
                SizedBox(height: 100),
                _buildNextPageButton('다음으로'),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildNextPageButton(String text) {
    return Container(
      height: 50,
      width: double.infinity,
      decoration: BoxDecoration(
        color: isButtonEnabled ? Color(0xFFC1004B) : Colors.white,
        borderRadius: BorderRadius.circular(10),
      ),
      child: TextButton(
        onPressed: isButtonEnabled
            ? () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => SendingPage2(
                senderName: _controllerFactory.getController('senderName').text,
                receiverName: _controllerFactory.getController('receiverName').text,
                senderRegion: _controllerFactory.getController('senderRegion').text,
                receiverRegion: _controllerFactory.getController('receiverRegion').text,
              ),
            ),
          );
        }
            : null,
        child: Text(
          text,
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600),
        ),
      ),
    );
  }

  Widget _buildTextField(String hintText, String controllerName) {
    return TextField(
      controller: _controllerFactory.getController(controllerName),
      decoration: InputDecoration(
        hintText: hintText,
        filled: true,
        fillColor: Colors.white,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: BorderSide(color: Colors.grey[300]!), // 테두리를 연한 회색으로 설정
        ),
      ),
    );
  }
}