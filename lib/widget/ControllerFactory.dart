import 'package:flutter/material.dart';

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