// To parse this JSON data, do
//
//     final sensorResponse = sensorResponseFromMap(jsonString);

import 'dart:convert';

List<SensorResponse> sensorResponseFromMap(String str) => List<SensorResponse>.from(json.decode(str).map((x) => SensorResponse.fromMap(x)));

class SensorResponse {
  SensorResponse({
    required this.id,
    required this.value,
    required this.feedId,
    required this.feedKey,
    required this.createdAt,
    required this.createdEpoch,
    required this.expiration,
  });

  final String id;
  final String value;
  final int feedId;
  final String feedKey;
  final DateTime createdAt;
  final int createdEpoch;
  final DateTime expiration;

  factory SensorResponse.fromMap(Map<String, dynamic> json) => SensorResponse(
    id: json["id"],
    value: json["value"],
    feedId: json["feed_id"],
    feedKey: json["feed_key"],
    createdAt: DateTime.parse(json["created_at"]),
    createdEpoch: json["created_epoch"],
    expiration: DateTime.parse(json["expiration"]),
  );

}
