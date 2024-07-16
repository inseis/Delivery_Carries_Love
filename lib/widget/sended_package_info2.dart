import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/services.dart';
import 'cost_view_page.dart';
import 'decorator.dart';

class SendingPage2 extends StatefulWidget {
  final String senderName;
  final String receiverName;
  final String senderRegion;
  final String receiverRegion;

  SendingPage2({
    required this.senderName,
    required this.receiverName,
    required this.senderRegion,
    required this.receiverRegion,
  });

  @override
  _SendingPage2State createState() => _SendingPage2State();
}

class _SendingPage2State extends State<SendingPage2> {
  final FirebaseDatabase _database = FirebaseDatabase.instance;

  final TextEditingController priceController = TextEditingController();
  final TextEditingController weightController = TextEditingController();

  String deliveryCompany = '한진택배';
  String deliveryInsurance = '유';
  String deliveryExpress = '일반';
  String deliveryRegion = '국내';

  List<String> domesticCompanies = ['한진택배', '롯데택배', '우체국택배', '로젠택배'];
  List<String> internationalCompanies = ['Amazon', 'DHL', 'EMS', 'FedEx'];

  int baseCost = 3000;
  int additionalCost = 0;
  int weightCost = 0;
  int insuranceCost = 0;
  int expressCost = 0;
  int deliveryTime = 0;

  @override
  void initState() {
    super.initState();
    priceController.addListener(_updateCostAndTime);
    weightController.addListener(_updateCostAndTime);
  }

  @override
  void dispose() {
    priceController.dispose();
    weightController.dispose();
    super.dispose();
  }

  void _updateCostAndTime() {
    setState(() {
      int price = int.tryParse(priceController.text) ?? 0;
      int weight = int.tryParse(weightController.text) ?? 0;

      additionalCost = (price > 5000) ? 500 : 0;
      weightCost = (weight >= 10) ? 2000 : 0;
      insuranceCost = (deliveryInsurance == '유') ? 10000 : 0;

      if (deliveryExpress == '익일') {
        expressCost = 5000;
        deliveryTime = 1;
      } else {
        expressCost = 0;
        deliveryTime = (deliveryRegion == '국내') ? 1 : 7;
        if (deliveryExpress == '일반') {
          deliveryTime += 1;
        }
      }
    });
  }

  int getTotalCost() {
    return baseCost + additionalCost + weightCost + insuranceCost + expressCost;
  }

  void _sendPackageDataToFirebase() {
    String senderKey = widget.senderName.replaceAll(' ', '_').toLowerCase(); // 공백을 밑줄로 치환하고 소문자로 변환

    _database.ref('packages/$senderKey').set({
      'senderName': widget.senderName,
      'receiverName': widget.receiverName,
      'senderRegion': widget.senderRegion,
      'receiverRegion': widget.receiverRegion,
      'price': priceController.text,
      'weight': weightController.text,
      'deliveryCompany': deliveryCompany,
      'deliveryInsurance': deliveryInsurance,
      'deliveryExpress': deliveryExpress,
      'deliveryRegion': deliveryRegion,
      'totalCost': getTotalCost(),
      'deliveryTime': deliveryTime,
    }).then((_) {
      print('Package sent successfully!');
    }).catchError((error) {
      print('Failed to send package: $error');
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
            fontWeight: FontWeight.w600,
          ),
        ),
        backgroundColor: Colors.white,
        centerTitle: true,
        iconTheme: IconThemeData(color: Colors.black),
      ),
      body: Container(
        color: Colors.white,
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
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
                TextFieldDecorator(
                  controller: priceController,
                  hintText: '물품의 가격 (원)',
                ),
                SizedBox(height: 20),
                TextFieldDecorator(
                  controller: weightController,
                  hintText: '물품의 무게 (kg)',
                ),
                SizedBox(height: 40),
                Divider(color: Colors.grey),
                _buildDropdown('국내/외 배송', deliveryRegion, <String>['국내', '해외'], (newValue) {
                  setState(() {
                    deliveryRegion = newValue;
                    deliveryCompany = deliveryRegion == '국내' ? domesticCompanies[0] : internationalCompanies[0];
                    deliveryExpress = '일반';
                    _updateCostAndTime();
                  });
                }),
                _buildDropdown('택배회사', deliveryCompany, deliveryRegion == '국내' ? domesticCompanies : internationalCompanies, (newValue) {
                  setState(() {
                    deliveryCompany = newValue;
                  });
                }),
                _buildDropdown('보험 유/무', deliveryInsurance, <String>['유', '무'], (newValue) {
                  setState(() {
                    deliveryInsurance = newValue;
                    _updateCostAndTime();
                  });
                }),
                _buildDropdown('택배배송방법', deliveryExpress, deliveryRegion == '국내' ? <String>['익일', '일반'] : <String>['일반'], (newValue) {
                  setState(() {
                    deliveryExpress = newValue;
                    _updateCostAndTime();
                  });
                }),
                Divider(color: Colors.grey),
                SizedBox(height: 20),
                Center(
                  child:Text(
                    '예상 운임 비용 : ${getTotalCost()}원',
                    style: TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 24,
                    ),
                  ),
                ),
                Center(
                  child:Text(
                      '예상 배달 시간 : $deliveryTime 일',
                      style: TextStyle(
                        fontWeight: FontWeight.w600,
                        fontSize: 24,
                      ),
                  ),
                ),
                SizedBox(height: 25),
                _buildNextPageButton('택배 보내기'),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildDropdown(String labelText, String currentValue, List<String> options, Function(String) onChanged) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(labelText),
        DropdownButton<String>(
          value: currentValue,
          icon: const Icon(Icons.arrow_drop_down_circle_outlined),
          iconSize: 24,
          elevation: 8,
          style: const TextStyle(color: Colors.black),
          onChanged: (String? newValue) {
            onChanged(newValue!);
          },
          items: options.map<DropdownMenuItem<String>>((String value) {
            return DropdownMenuItem<String>(
              value: value,
              child: Text(value),
            );
          }).toList(),
        ),
      ],
    );
  }

  Widget _buildNextPageButton(String text) {
    return Container(
      height: 50,
      width: double.infinity,
      decoration: BoxDecoration(
        color: Color(0xFFC1004B),
        border: Border.all(color: Colors.grey[300]!, width: 1),
        borderRadius: BorderRadius.circular(10),
      ),
      child: TextButton(
        onPressed: () {
          _sendPackageDataToFirebase();
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => CostViewPage(
                senderName: widget.senderName,
                receiverName: widget.receiverName,
                senderRegion: widget.senderRegion,
                receiverRegion: widget.receiverRegion,
                price: priceController.text,
                weight: weightController.text,
                deliveryCompany: deliveryCompany,
                deliveryInsurance: deliveryInsurance,
                deliveryExpress: deliveryExpress,
                deliveryRegion: deliveryRegion,
                totalCost: getTotalCost(),
                deliveryTime: deliveryTime,
              ),
            ),
          );
        },
        child: Text(
          text,
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    );
  }
}