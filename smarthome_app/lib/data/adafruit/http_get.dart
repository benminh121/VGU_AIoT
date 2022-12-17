import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:smarty/data/adafruit/sensor_response_model.dart';
import 'package:smarty/utils/enum_sensor.dart';

//make a provider for adafruit
final adafruitProvider = Provider.family((ref, Sensor sensor) => Adafruit(sensor: sensor));

class Adafruit {
  final Sensor sensor;

  const Adafruit({
    required this.sensor,
  });

  // get fist sensor response from http get
  Future<SensorResponse> httpGet() async {
    final String _url = 'https://io.adafruit.com/api/v2/tranlydongdong/feeds/${sensor.name}/data';
    var dio = Dio();
    dio.options.headers['X-AIO-Key'] =
    'aio_mVLt08wD3Nd2mVBdedDiZHFu4tJq';
    var res = await dio.get(_url);
    print(res.data[0]);
    return SensorResponse.fromMap(res.data[0]);
  }
}
