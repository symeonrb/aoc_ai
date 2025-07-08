class WeatherData {
  final DateTime datetime;
  final double temperature;
  final double humidity;
  final double pressure;
  final double wind;
  final double cloudiness;
  final double nextHourTemperature;

  WeatherData({
    required this.datetime,
    required this.temperature,
    required this.humidity,
    required this.pressure,
    required this.wind,
    required this.cloudiness,
    required this.nextHourTemperature,
  });

  factory WeatherData.fromRow(List<dynamic> row) {
    return WeatherData(
      datetime: DateTime.parse(row[0].toString()),
      temperature: (row[1] is num)
          ? row[1].toDouble()
          : double.parse(row[1].toString()),
      humidity: (row[2] is num)
          ? row[2].toDouble()
          : double.parse(row[2].toString()),
      pressure: (row[3] is num)
          ? row[3].toDouble()
          : double.parse(row[3].toString()),
      wind: (row[4] is num)
          ? row[4].toDouble()
          : double.parse(row[4].toString()),
      cloudiness: (row[5] is num)
          ? row[5].toDouble()
          : double.parse(row[5].toString()),
      nextHourTemperature: (row[6] is num)
          ? row[6].toDouble()
          : double.parse(row[6].toString()),
    );
  }

  @override
  String toString() {
    return 'WeatherData(datetime: $datetime, temperature: $temperature, humidity: $humidity, pressure: $pressure, wind: $wind, cloudiness: $cloudiness, nextHourTemperature: $nextHourTemperature)';
  }
}
