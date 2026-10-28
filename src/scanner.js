'use strict';

const { parseTasks } = require('./parser');

// Поддерживаем JS/TS и исходники/заголовки C++ (включая разные расширения).
const FILE_GLOB = '**/*.{js,jsx,mjs,cjs,ts,tsx,cpp,cc,cxx,h,hpp,hh,hxx}';
const EXCLUDE_GLOB = '**/{node_modules,.git,dist,build,coverage,out,.next}/**';
const SUPPORTED_FILE = /\.(?:js|jsx|mjs|cjs|ts|tsx|cpp|cc|cxx|h|hpp|hh|hxx)$/i;

/**
 * Сканируем проект через API редактора: это работает и с несколькими корнями
 * рабочей области, и с файловыми системами, которые поддерживает VS Code.
 */
async function scanWorkspace(vscode) {
  const found = [];
  const uris = await vscode.workspace.findFiles(FILE_GLOB, EXCLUDE_GLOB);

  for (const uri of uris) {
    try {
      const bytes = await vscode.workspace.fs.readFile(uri);
      const content = Buffer.from(bytes).toString('utf8');
      const tasks = parseTasks(content);

      for (const task of tasks) {
        found.push({ ...task, uri });
      }
    } catch (error) {
      // Ошибка чтения одного файла не должна прерывать поиск в остальных.
      console.warn(`TODO Navigator: не удалось прочитать ${uri.toString()}`, error);
    }
  }

  return found;
}

module.exports = { scanWorkspace, SUPPORTED_FILE, FILE_GLOB, EXCLUDE_GLOB };
