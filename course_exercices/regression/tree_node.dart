import 'dart:math';

import 'mse.dart';

class TreeNode<T> {
  TreeNode(
    this.population,
    this.getMainAttribute,
    this.mse,
    Map<String, bool Function(T)> selectors,
  ) : _selectors = selectors,
      deepness = 0 {
    _createChildren();
  }

  TreeNode._temp(
    this.population,
    this.getMainAttribute,
    this.mse,
    this.deepness,
    Map<String, bool Function(T)> selectors,
  ) : _selectors = selectors;

  final List<T> population;
  final double Function(T) getMainAttribute;
  final double mse;
  final Map<String, bool Function(T)> _selectors;
  final int deepness;
  late final List<TreeNode<T>> children;
  late final String childrenSelector;

  @override
  String toString() =>
      'TreeNode(pop:${population.length}, '
      'mse:$mse, '
      '${children.isEmpty ? 'mainAtt:$mainAtt' : 'childrenSelector:$childrenSelector'})';

  double get mainAtt {
    final mainAttsMap = <double, int>{};
    for (final data in population) {
      final mainAtt = getMainAttribute(data);
      mainAttsMap[mainAtt] ??= 0;
      mainAttsMap[mainAtt] = mainAttsMap[mainAtt]! + 1;
    }
    final entries = mainAttsMap.entries.toList()
      ..sort((a, b) => a.value.compareTo(b.value));
    return entries.last.key;
  }

  (TreeNode<T>, TreeNode<T>) _split(bool Function(T) getValue) {
    // final mainAtts = population.map(getMainAttribute).toSet();

    // Split data into two groups based on the boolean function
    final truePop = population.where(getValue);
    final falsePop = population.where((data) => !getValue(data));

    // final trueGroup = <double>[];
    // final falseGroup = <double>[];
    // for (final data in population) {
    //   (getValue(data) ? trueGroup : falseGroup).add(getMainAttribute(data));
    // }

    // print(categories);
    // print(
    //   categories
    //       .map((cat) => trueGroup.where((value) => value == cat).length)
    //       .toList(),
    // );
    // print(
    //   categories
    //       .map((cat) => falseGroup.where((value) => value == cat).length)
    //       .toList(),
    // );

    return (
      TreeNode._temp(
        truePop.toList(),
        getMainAttribute,
        calcMse(truePop.map(getMainAttribute)),
        deepness + 1,
        _selectors,
      ),
      TreeNode._temp(
        falsePop.toList(),
        getMainAttribute,
        calcMse(falsePop.map(getMainAttribute)),
        deepness + 1,
        _selectors,
      ),
    );
  }

  void _createChildren() {
    // final mainAtts = population.map(getMainAttribute).toSet();
    if (deepness > 1) {
      // This is a leaf (1) or population is empty (0)
      children = [];
      childrenSelector = '';
      // print(
      //   'TreeNode(pop:${population.length}, mse:$mse, childrenSelector:$childrenSelector)',
      // );
      return;
    }

    // print('_createChildren, ${categories.length}');

    var min_ = double.infinity;
    var selectedSelector = _selectors.entries.first;
    (TreeNode<T>, TreeNode<T>)? selectedNodes;

    // print('---');
    for (final entry in _selectors.entries) {
      final nodes = _split(entry.value);
      if (nodes.$1.population.isEmpty || nodes.$2.population.isEmpty) {
        continue;
      }
      if (nodes.$1.mse == 0 || nodes.$2.mse == 0) {
        continue;
      }
      final score = nodes.$1.mse + nodes.$2.mse;
      // print('${entry.key} : ${nodes.$1.mse}, ${nodes.$2.mse}');
      if (score < min_) {
        min_ = score;
        selectedSelector = entry;
        selectedNodes = nodes;
      }
    }

    if (selectedNodes == null) {
      // This is a leaf with multiple categories
      children = [];
      childrenSelector = '';
      // print(
      //   'TreeNode(pop:${population.length}, mse:$mse, childrenSelector:$childrenSelector)',
      // );
      return;
    }

    children = [selectedNodes.$1, selectedNodes.$2];
    childrenSelector = selectedSelector.key;

    if (children.any((c) => c.population.length == 0)) {
      throw Exception();
    }

    // print(
    //   'TreeNode(pop:${population.length}, mse:$mse, childrenSelector:$childrenSelector)',
    // );

    for (final child in children) {
      child._createChildren();
    }
  }

  String prettyPrint([
    String indent = '',
    bool isLast = true,
    String? branchLabel,
  ]) {
    final buffer = StringBuffer();
    final connector = indent.isEmpty ? '' : (isLast ? '└── ' : '├── ');
    final branchInfo = branchLabel != null ? '[$branchLabel] ' : '';

    final allCats = population.map(getMainAttribute).toSet();
    final repartition = allCats
        .map(
          (cat) => population
              .where((value) => getMainAttribute(value) == cat)
              .length,
        )
        .toList();

    if (children.isEmpty) {
      // Leaf node: show main category and population size
      var ln =
          '$indent$connector$branchInfo[LEAF] pop:${population.length} mainAtt:$mainAtt '
          'mse:${mse.toStringAsFixed(4)} ';
      if (mse >= 0) {
        // ln += 'allCats:$allCats$repartition ';
        // ln +=
        //     population.map((a) => (a as WeatherData).species).toList().toString() +
        //     ' ';
      }
      buffer.writeln(ln);
    } else {
      buffer.writeln(
        '$indent$connector$branchInfo$childrenSelector? (pop:${population.length}, mse:${mse.toStringAsFixed(4)}) ',
        // 'allCats:$allCats$repartition ',
      );
      for (var i = 0; i < children.length; i++) {
        final child = children[i];
        final nextIndent = indent + (isLast ? '    ' : '│   ');
        final label = i == 0 ? 'true' : 'false';
        buffer.write(
          child.prettyPrint(nextIndent, i == children.length - 1, label),
        );
      }
    }
    return buffer.toString();
  }
}
