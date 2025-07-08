import 'dart:io';
import 'package:excel/excel.dart';

import 'mse.dart';
import 'tree_node.dart';
import 'weather_data.dart';

void main() async {
  final file = File('weather_dataset_10.xlsx');
  final bytes = await file.readAsBytes();
  final excel = Excel.decodeBytes(bytes);

  for (var table in excel.tables.keys) {
    // print('Sheet: $table');
    final sheet = excel.tables[table]!;
    if (sheet.rows.isEmpty) continue;
    final dataRows = sheet.rows.skip(1);
    final weatherDataList = <WeatherData>[];
    for (var row in dataRows) {
      final values = row.map((cell) => cell?.value).toList();
      if (values.length < 7 || values.any((v) => v == null)) continue;
      try {
        final weatherData = WeatherData.fromRow(values);
        weatherDataList.add(weatherData);
        // print(weatherData);
      } catch (e) {
        print('Error parsing row: $values -> $e');
      }
    }

    // print('Total WeatherData objects: ${weatherDataList.length}');

    final root = TreeNode(
      weatherDataList,
      (a) => a.temperature,
      calcMse(weatherDataList.map((a) => a.temperature)),
      {
        'hot': (WeatherData a) => a.temperature > 23.0,
        'pressure': (WeatherData a) => a.pressure > 1012.0,
        'pressure3': (WeatherData a) => a.pressure > 1014.0,
        'pressure5': (WeatherData a) => a.pressure > 1010.0,
        'pressure2': (WeatherData a) => a.pressure > 1018.0,
        'cloudy': (WeatherData a) => a.cloudiness > 30.0,
        'cloudy2': (WeatherData a) => a.cloudiness > 20.0,
        'cloudy3': (WeatherData a) => a.cloudiness > 40.0,
        'cloudy4': (WeatherData a) => a.cloudiness > 50.0,
        'windy': (WeatherData a) => a.wind > 4.0,
        'windy2': (WeatherData a) => a.wind > 2.0,
        'windy3': (WeatherData a) => a.wind > 6.0,
      },
    );
    print(root.prettyPrint());
  }
}
