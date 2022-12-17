enum Sensor {
  sensorTemperature,
  sensorHumidity,
}

extension SensorType on Sensor {
  String get name {
    switch (this) {
      case Sensor.sensorTemperature:
        return 'sensor1';
      case Sensor.sensorHumidity:
        return 'sensor2';
    }
  }
}
