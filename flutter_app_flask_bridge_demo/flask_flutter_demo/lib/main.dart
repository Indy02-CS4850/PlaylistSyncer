import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class BackendBloc extends Cubit<String> {
  BackendBloc() : super('');

  Future<void> fetchData() async {
    final response = await http.get(Uri.parse('http://99.8.194.130:5000/api'));
    if (response.statusCode == 200) {
      emit(response.body);
    } else {
      emit('Failed to fetch data');
    }
  }
}

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: BlocProvider(
        create: (context) => BackendBloc(),
        child: MyWidget(),
      ),
    );
  }
}

class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final backendBloc = BlocProvider.of<BackendBloc>(context);

    return Scaffold(
      appBar: AppBar(
        title: Text('Flutter App with Python Backend'),
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