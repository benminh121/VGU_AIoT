import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:smarty/data/adafruit/sensor_response_model.dart';
import 'package:smarty/utils/enum_sensor.dart';

import '../../../../core/navigation/navigator.dart';
import '../../../../data/adafruit/http_get.dart';
import '../../../../shared/res/res.dart';

class SummaryHeader extends ConsumerWidget {
  const SummaryHeader({
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return GestureDetector(
      onTap: () => AppNavigator.pushNamed(routineRoute),
      child: Container(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 8),
        decoration: BoxDecoration(
          color: SmartyColors.primary,
          borderRadius: BorderRadius.circular(6.0),
        ),
        child: FutureBuilder(
            future: ref.watch(adafruitProvider(Sensor.sensorTemperature)).httpGet(),
            builder: (context, AsyncSnapshot<SensorResponse> asyncSnapshot) {
              return Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
                Column(
                  children: [
                    Text(
                      'Temperature',
                      style: TextStyles.body.copyWith(color: SmartyColors.tertiary),
                    ),
                    Row(
                      children: [
                        Icon(
                          Icons.thermostat,
                          size: 24,
                          color: SmartyColors.tertiary,
                        ),
                        asyncSnapshot.connectionState == ConnectionState.waiting
                            ? const Text('Loading...')
                            : Text(
                                '${asyncSnapshot.data?.value}°C',
                                style: TextStyles.body.copyWith(color: SmartyColors.tertiary),
                              ),
                      ],
                    )
                  ],
                ),
                FutureBuilder(
                    future: ref.watch(adafruitProvider(Sensor.sensorHumidity)).httpGet(),
                    builder: (context, AsyncSnapshot<SensorResponse> asyncSnapshot) {
                      print(asyncSnapshot.data?.value);
                      return Column(
                        children: [
                          Text(
                            'Humidity',
                            style: TextStyles.body.copyWith(color: SmartyColors.tertiary),
                          ),
                          Row(
                            children: [
                              Icon(
                                Icons.water_drop_outlined,
                                size: 24,
                                color: SmartyColors.tertiary,
                              ),
                              asyncSnapshot.connectionState == ConnectionState.waiting
                                  ? const Text('Loading...')
                                  : Text(
                                      '${asyncSnapshot.data?.value}%',
                                      style: TextStyles.body.copyWith(color: SmartyColors.tertiary),
                                    ),
                            ],
                          ),
                        ],
                      );
                    }),
                Column(
                  children: [
                    Text(
                      'Energy Used',
                      style: TextStyles.body.copyWith(color: SmartyColors.tertiary),
                    ),
                    Row(
                      children: [
                        Icon(
                          Icons.bolt_sharp,
                          size: 24,
                          color: SmartyColors.tertiary,
                        ),
                        Text(
                          '250 KWh',
                          style: TextStyles.body.copyWith(color: SmartyColors.tertiary),
                        ),
                      ],
                    )
                  ],
                ),
              ]);
            }),
      ),
    );
  }
}
