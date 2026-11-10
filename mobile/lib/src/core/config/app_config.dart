class AppConfig {
  AppConfig._();

  // Override with --dart-define=API_BASE_URL=http://10.0.2.2:8000/v1
  static const apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000/v1',
  );
  static const supportedLocales = ['en', 'hi'];
}
