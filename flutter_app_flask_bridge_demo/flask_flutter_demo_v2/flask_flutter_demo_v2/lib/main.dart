import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class BackendBloc extends Cubit<String> {
  BackendBloc() : super('');

  Future<void> fetchData() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:5000/api')); //change this to reflect local host of server host (99.8.194.130)
    if (response.statusCode == 200) {
      emit(response.body);
    } else {
      emit('Failed to fetch data');
    }
  }
}

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: BlocProvider(
        create: (context) => BackendBloc(),
        child: const MyWidget(),
      ),
    );
  }
}

class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final backendBloc = BlocProvider.of<BackendBloc>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter App with Python Backend'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            backendBloc.fetchData();
          },
          child: BlocBuilder<BackendBloc, String>(
          builder: (context, state) {
            return Text(state);
          },
        ),
        ),
      ),
    );
  }
}