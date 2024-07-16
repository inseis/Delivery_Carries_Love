import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

class DataNotifier extends ChangeNotifier {
  bool _isButtonEnabled = false;

  bool get isButtonEnabled => _isButtonEnabled;

  void validateFields(List<TextEditingController> controllers) {
    _isButtonEnabled = controllers.every((controller) => controller.text.isNotEmpty);
    notifyListeners();
  }
}