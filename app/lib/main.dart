import 'package:flutter/material.dart';

void main() => runApp(const TerritorioVivoApp());

/// Shell de seguranca: ainda NAO executa coleta de dados reais.
/// Qualquer funcionalidade so sera exposta apos implementar e validar gates.
class TerritorioVivoApp extends StatelessWidget {
  const TerritorioVivoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Território Vivo | Campo',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF246654)),
      ),
      home: const SafetyLandingPage(),
    );
  }
}

class SafetyLandingPage extends StatelessWidget {
  const SafetyLandingPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Território Vivo')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            Card(
              color: Theme.of(context).colorScheme.errorContainer,
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(
                      children: [
                        Icon(Icons.warning_amber_rounded),
                        SizedBox(width: 9),
                        Text(
                          'NÃO LIBERADO PARA CAMPO',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      'Esta versão é apenas um esqueleto técnico. '
                      'Ela não registra áudio, fotos nem observações. '
                      'Use o kit físico e as ferramentas nativas autorizadas.',
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 18),
            Text('Três camadas obrigatórias',
                style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 10),
            const _GateTile(
              icon: Icons.save_alt,
              title: '1. Persistência local',
              caption: 'Gravar, reabrir e conferir conteúdo e SHA-256.',
            ),
            const _GateTile(
              icon: Icons.backup,
              title: '2. Cópia independente',
              caption: 'Exportação protegida para outro meio físico.',
            ),
            const _GateTile(
              icon: Icons.fact_check,
              title: '3. Restauração verificada',
              caption: 'Recuperar arquivos e conferir hashes fora da origem.',
            ),
            const SizedBox(height: 12),
            Text('Plano de contingência',
                style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 8),
            const ExpansionTile(
              initiallyExpanded: true,
              title: Text('Se o aplicativo não estiver disponível'),
              leading: Icon(Icons.assignment_outlined),
              children: [
                ListTile(
                  title: Text('Registro manual'),
                  subtitle: Text(
                    'Fichas numeradas, caderno de campo, mapa falado '
                    'e árvore de problemas em papel.',
                  ),
                ),
                ListTile(
                  title: Text('Mídias com autorização'),
                  subtitle: Text(
                    'Usar gravador e câmera nativos, anotando '
                    'o vínculo com o código da sessão em papel.',
                  ),
                ),
                ListTile(
                  title: Text('Ao encerrar'),
                  subtitle: Text(
                    'Conferir originais, copiar em outro meio '
                    'e testar a recuperação antes de descartar qualquer cópia.',
                  ),
                ),
              ],
            ),
            const SizedBox(height: 22),
            const Text(
              'Todo relato, mapa e árvore deve ser validado com a comunidade. '
              'O aplicativo não define limites territoriais oficiais.',
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}

class _GateTile extends StatelessWidget {
  const _GateTile({
    required this.icon,
    required this.title,
    required this.caption,
  });
  final IconData icon;
  final String title;
  final String caption;
  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Icon(icon),
        title: Text(title),
        subtitle: Text(caption),
        trailing: const Icon(Icons.lock_outline),
      ),
    );
  }
}
