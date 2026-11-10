import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('The Tech World'),
        actions: [
          IconButton(
            tooltip: 'Profile',
            onPressed: () {},
            icon: const Icon(Icons.account_circle_outlined),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text('Learn something new today',
              style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 8),
          Text('अपनी सीखने की यात्रा शुरू करें',
              style: Theme.of(context).textTheme.bodyLarge),
          const SizedBox(height: 24),
          TextField(
            decoration: InputDecoration(
              hintText: 'Search courses / कोर्स खोजें',
              prefixIcon: const Icon(Icons.search),
              filled: true,
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(16),
                borderSide: BorderSide.none,
              ),
            ),
          ),
          const SizedBox(height: 24),
          Text('Explore courses', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 12),
          const _CoursePlaceholder(
            title: 'Start learning',
            subtitle: 'Courses in English and Hindi will appear here.',
            icon: Icons.menu_book_outlined,
          ),
          const SizedBox(height: 12),
          const _CoursePlaceholder(
            title: 'Your learning journey',
            subtitle: 'Subscribe monthly to unlock the full library.',
            icon: Icons.school_outlined,
          ),
        ],
      ),
    );
  }
}

class _CoursePlaceholder extends StatelessWidget {
  const _CoursePlaceholder({
    required this.title,
    required this.subtitle,
    required this.icon,
  });

  final String title;
  final String subtitle;
  final IconData icon;

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: CircleAvatar(child: Icon(icon)),
        title: Text(title),
        subtitle: Text(subtitle),
      ),
    );
  }
}
