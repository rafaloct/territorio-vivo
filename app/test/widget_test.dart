import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:territorio_vivo_campo/main.dart';

void main() {
  testWidgets('prototype never claims field readiness', (tester) async {
    await tester.pumpWidget(const TerritorioVivoApp());
    expect(find.text('NÃO LIBERADO PARA CAMPO'), findsOneWidget);
    expect(find.text('Três camadas obrigatórias'), findsOneWidget);
    expect(find.byIcon(Icons.lock_outline), findsNWidgets(3));
    expect(find.textContaining('Esta versão é apenas'), findsOneWidget);
  });
}
