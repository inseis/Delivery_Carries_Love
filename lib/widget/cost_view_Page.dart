import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../main.dart';

class CostViewPage extends StatefulWidget {
  final String senderName;
  final String receiverName;
  final String senderRegion;
  final String receiverRegion;
  final String price;
  final String weight;
  final String deliveryCompany;
  final String deliveryInsurance;
  final String deliveryExpress;
  final String deliveryRegion;
  final int totalCost;
  final int deliveryTime;

  CostViewPage({
    required this.senderName,
    required this.receiverName,
    required this.senderRegion,
    required this.receiverRegion,
    required this.price,
    required this.weight,
    required this.deliveryCompany,
    required this.deliveryInsurance,
    required this.deliveryExpress,
    required this.deliveryRegion,
    required this.totalCost,
    required this.deliveryTime,
  });

  @override
  _CostViewPageState createState() => _CostViewPageState();
}

class _CostViewPageState extends State<CostViewPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          '택배 보내기',
          style: TextStyle(color: Colors.black),
        ),
        backgroundColor: Colors.white,
        centerTitle: true,
        iconTheme: IconThemeData(color: Colors.black),
      ),
      body: Container(
        color: Colors.white,
        child:Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20.0),
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(height: 40),
                  Text(
                    '택배는 사랑을 싣고',
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    '사랑을 나누는 택배 서비스',
                    style: TextStyle(fontSize: 18, color: Colors.grey),
                  ),
                  SizedBox(height: 40),
                  Center(
                    child: Text(
                      '입력하신 정보가 맞는 지 확인해주세요.',
                      style: TextStyle(fontSize: 16, color: Colors.grey[400]),
                    ),
                  ),
                  SizedBox(height: 20),
                  _buildInfoRow('보낸 사람', widget.senderName),
                  Divider(color: Colors.grey),
                  _buildInfoRow('받는 사람', widget.receiverName),
                  Divider(color: Colors.grey),
                  _buildInfoRow('보낸 지역', widget.senderRegion),
                  Divider(color: Colors.grey),
                  _buildInfoRow('받는 지역', widget.receiverRegion),
                  Divider(color: Colors.grey),
                  _buildInfoRow('물품 가격', '${widget.price} 원'),
                  Divider(color: Colors.grey),
                  _buildInfoRow('물품 무게', '${widget.weight} kg'),
                  Divider(color: Colors.grey),
                  _buildInfoRow('택배 회사', widget.deliveryCompany),
                  Divider(color: Colors.grey),
                  _buildInfoRow('보험 유무', widget.deliveryInsurance),
                  Divider(color: Colors.grey),
                  _buildInfoRow('배송 방법', widget.deliveryExpress),
                  Divider(color: Colors.grey),
                  _buildInfoRow('배송 지역', widget.deliveryRegion),
                  Divider(color: Colors.grey),

                  SizedBox(height: 25),
                  _buildInfoCost('예상 운임 비용', '${widget.totalCost} 원'),
                  _buildInfoCost('예상 소요 시간', '${widget.deliveryTime} 일'),
                  SizedBox(height: 45),
                  Center(child: _buildNextPageButton('택배 보내기')),
                ],
              ),
            ),
          ),
        ),
      )

    );
  }
  Widget _buildInfoCost(String label, String value) {
    return Container(
      margin: EdgeInsets.only(left: 25),
      child: Center(
        child: Row(
          children: [
            Text(
              label,
              style: TextStyle(fontSize: 24, color: Colors.black, fontWeight: FontWeight.w600),
            ),
            SizedBox(width: 40),
            Text(
              value,
              style: TextStyle(fontSize: 24, color: Colors.black),
            ),
          ],
        ),
      ),
    );
  }
  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: TextStyle(fontSize: 16, color: Colors.black),
          ),
          Text(
            value,
            style: TextStyle(fontSize: 16, color: Colors.black),
          ),
        ],
      ),
    );
  }

  Widget _buildNextPageButton(String text) {
    return Container(
      height: 40,
      width: 200,
      decoration: BoxDecoration(
        color: Color(0xFFC1004B),
        borderRadius: BorderRadius.circular(10),
      ),
      child: TextButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => MyApp()),
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