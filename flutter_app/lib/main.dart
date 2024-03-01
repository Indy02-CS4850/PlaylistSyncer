import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomePage(),
      theme: ThemeData(
        brightness: Brightness.dark,
      )
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
	  return Scaffold(
	    appBar: AppBar(
		    title: const Text('GeeksForGeeks'),
		    backgroundColor: Colors.green,
	    ),
	    body: Stack(
        children:  <Widget>[
          Align(alignment: Alignment.bottomLeft,
            child: FloatingActionButton(
              heroTag: "Transfer",
              elevation: 20.0,
              child: const Icon(Icons.send_and_archive),
		          onPressed: () {
		            Navigator.of(context).push(_createRoutePage2());
		          },
	          ), 
          ),
          Align(alignment: Alignment.bottomRight,
            child: FloatingActionButton(
              heroTag: "Settings",
              elevation: 20.0,
              child: const Icon(Icons.settings),
		          onPressed: () {
		            Navigator.of(context).push(_createRoutePage3());
		          },
	          ), 
          ),
          Center(
            child: ElevatedButton(
              onPressed: () {
                Navigator.of(context).push(_createRoutePage4());
              }, 
              child: const Text("Form Test"),
              ),
          ),

        ],
      ),
		// RaisedButton is deprecated
		// We should use ElevatedButton instead

		// child: RaisedButton(
		// child: const Text('Go to Page 2'),
		// onPressed: () {
		//	 Navigator.of(context).push(_createRoute());
		// },
		// ),
    
	  );
  }
}

// This page is for transfer
Route _createRoutePage2() {
  return PageRouteBuilder(
	  pageBuilder: (context, animation, secondaryAnimation) =>  const Page2(),
	  transitionsBuilder: (context, animation, secondaryAnimation, child) {
	    var begin = const Offset(0.0, 1.0);
	    var end = Offset.zero;
	    var curve = Curves.ease;

	    var tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));

	    return SlideTransition(
		    position: animation.drive(tween),
		    child: child,
	    );
	  },
  );
}

// This page is for transfer
class Page2 extends StatelessWidget {
  const Page2({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
	  return Scaffold(
	    appBar: AppBar(),
	      body: Center(
		      child: MyDropdown(),
	    ),
	  );
  }
}

// I am thinking what we do for selecting a playlist is make another drop down
// once the user has selected what they want to transfer from that is just a list
// of playlist names off that platform.

class MyDropdown extends StatefulWidget {
  @override
  _MyDropdownState createState() => _MyDropdownState();
}

class _MyDropdownState extends State<MyDropdown> {
  List<String> dropdownItems = ['Spotify', 'Youtube Music', 'Apple Music'];
  String? selectedItem = '';
  String hintText = 'What do you want to transfer from?';
  List<String> PlatformFrom = [];
  List<String> PlatformTo = [];

  @override
  Widget build(BuildContext context) {
    return DropdownButton<String>(
      value: dropdownItems.contains(selectedItem) ? selectedItem : null ,
      hint: Text(hintText),
      items: dropdownItems.map((String value) {
        return DropdownMenuItem<String> (
          value: value,
          child: Text(value),
          );
      }).toList(),
      onChanged: (String? newValue) {
        setState((){
          hintText = 'What do you want to transfer to?';
          selectedItem = newValue;
          dropdownItems.remove(newValue);
          if(newValue != null){ // This is used to keep track of what has been selected
            if(PlatformFrom.isEmpty){
              PlatformFrom.add(newValue);
              print('From : $PlatformFrom'); // Testing Purposes
            }
            else{
              PlatformTo.add(newValue);
              print('From : $PlatformTo'); // Testing Purposes
            }
          }
        });
      },
    );
  }
}


// This page is for settings
Route _createRoutePage3() {
  return PageRouteBuilder(
	  pageBuilder: (context, animation, secondaryAnimation) => Page3(),
	  transitionsBuilder: (context, animation, secondaryAnimation, child) {
	    var begin = const Offset(0.0, 1.0);
	    var end = Offset.zero;
	    var curve = Curves.ease;

	    var tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));

	    return SlideTransition(
		    position: animation.drive(tween),
		    child: child,
	    );
	  },
  );
}

// This page is for settings
class Page3 extends StatelessWidget {
  Page3({Key? key}) : super(key: key);
  final ValueNotifier<ThemeMode> _notifier = ValueNotifier(ThemeMode.light);

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: _notifier,
      builder: (_, mode, __) {
        return Scaffold(
	        appBar: AppBar(),
	        body: Center(
	          child: ElevatedButton(
              onPressed: () => _notifier.value = mode == ThemeMode.light ? ThemeMode.dark : ThemeMode.light,
              child: Text('Toggle Theme'),
            ),
          )
        );
      }
    );
  }
}

// This page is for sign in submission forms
Route _createRoutePage4() {
  return PageRouteBuilder(
	  pageBuilder: (context, animation, secondaryAnimation) => Page4(),
	  transitionsBuilder: (context, animation, secondaryAnimation, child) {
	    var begin = const Offset(0.0, 1.0);
	    var end = Offset.zero;
	    var curve = Curves.ease;

	    var tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));

	    return SlideTransition(
		    position: animation.drive(tween),
		    child: child,
	    );
	  },
  );
}

// This page is for sign in submission forms
class Page4 extends StatelessWidget {
  Page4({Key? key}) : super(key: key);
  var _formKey = GlobalKey<FormState>(); 
  var isLoading = false; 
  
  void _submit() { 
    final isValid = _formKey.currentState!.validate(); 
    if (!isValid) { 
      return; 
    } 
    _formKey.currentState!.save(); 
  }
  @override
  Widget build(BuildContext context) {
	  return Scaffold(
	    appBar: AppBar(),
	    body: Center(
		    child: Form( 
          key: _formKey, 
          child: Column( 
            children: <Widget>[ 
              const Text( 
                "Form-Validation In Flutter ", 
                style: TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold), 
              ), 
              //styling 
              SizedBox( 
                height: MediaQuery.of(context).size.width * 0.1, 
              ), 
              TextFormField( 
                decoration: const InputDecoration(labelText: 'E-Mail'), 
                keyboardType: TextInputType.emailAddress, 
                onFieldSubmitted: (value) { 
                  //Validator 
                }, 
                validator: (value) { 
                  if (value!.isEmpty || !RegExp(r"^[a-zA-Z0-9.a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9]+\.[a-zA-Z]+").hasMatch(value)) { 
                    return 'Enter a valid email!'; 
                  } 
                  return null; 
                }, 
              ), 
              //box styling 
              SizedBox( 
                height: MediaQuery.of(context).size.width * 0.1, 
              ), 
              //text input  
              TextFormField( 
                // ignore: prefer_const_constructors
                decoration: InputDecoration(labelText: 'Password'), 
                keyboardType: TextInputType.emailAddress, 
                onFieldSubmitted: (value) {}, 
                obscureText: true, 
                validator: (value) { 
                  if (value!.isEmpty) { 
                    return 'Enter a valid password!'; 
                  } 
                  return null; 
                }, 
              ), 
              SizedBox( 
                height: MediaQuery.of(context).size.width * 0.1, 
              ), 
              ElevatedButton(  
                child: const Text("Submit", 
                  style: TextStyle( 
                    fontSize: 24.0, 
                  ), 
                ), 
                onPressed: () => _submit(), 
              ) 
            ], 
          ), 
        ),
	    ),
	  );
  }
}
