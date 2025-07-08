import 'dart:math';

double calcMse(Iterable<double> mainAtts) {
  if (mainAtts.isEmpty) return 0.0;
  final mean = mainAtts.reduce((a, b) => a + b) / mainAtts.length;

  return mainAtts
          .map((value) => pow(value + -mean, 2))
          .fold(0.0, (a, b) => a + b) /
      mainAtts.length;
}
