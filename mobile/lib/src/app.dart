import 'package:flutter/material.dart';
import 'features/home/presentation/home_screen.dart';

class TheTechWorldApp extends StatelessWidget {
  const TheTechWorldApp({super.key});

  @override
  Widget build(BuildContext context) {
    const brand = Color(0xFF5B4BDB);
    return MaterialApp(
      title: 'The Tech World',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: brand),
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFF8F8FC),
      ),
      home: const HomeScreen(),
    );
  }
}
