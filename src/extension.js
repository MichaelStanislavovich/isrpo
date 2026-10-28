'use strict';

const vscode = require('vscode');
const { scanWorkspace, SUPPORTED_FILE } = require('./scanner');
const { TaskTreeProvider } = require('./tree');

/** Точка входа. VS Code вызывает activate при открытии представления. */
function activate(context) {
  const provider = new TaskTreeProvider();
  const view = vscode.window.createTreeView('todoNavigator.tasks', {
    treeDataProvider: provider,
    showCollapseAll: true
  });

  let scanVersion = 0;

  async function refresh() {
    // Если запущены несколько поисков, используем результат самого нового.
    const version = ++scanVersion;
    try {
      const tasks = await scanWorkspace(vscode);
      if (version !== scanVersion) {
        return;
      }
      provider.setTasks(tasks);
      updateViewDescription();
    } catch (error) {
      vscode.window.showErrorMessage(`TODO Navigator: ошибка поиска: ${String(error)}`);
    }
  }

  function updateViewDescription() {
    const count = provider.getVisibleCount();
    view.description = `${count} задач`;
    view.message = count === 0 ? 'Задач по выбранным фильтрам не найдено.' : undefined;
  }

  async function chooseType() {
    const selected = await vscode.window.showQuickPick([
      { label: 'Все типы', value: 'all' },
      { label: 'TODO', value: 'TODO' },
      { label: 'FIXME', value: 'FIXME' }
    ], { placeHolder: 'Фильтр по типу задачи' });

    if (selected) {
      provider.setTypeFilter(selected.value);
      updateViewDescription();
    }
  }

  async function choosePriority() {
    const selected = await vscode.window.showQuickPick([
      { label: 'Все приоритеты', value: 'all' },
      { label: 'high — высокий', value: 'high' },
      { label: 'medium — средний', value: 'medium' },
      { label: 'low — низкий', value: 'low' }
    ], { placeHolder: 'Фильтр по приоритету' });

    if (selected) {
      provider.setPriorityFilter(selected.value);
      updateViewDescription();
    }
  }

  async function openTask(task) {
    const document = await vscode.workspace.openTextDocument(task.uri);
    const position = new vscode.Position(task.line, 0);
    const range = new vscode.Range(position, position);
    const editor = await vscode.window.showTextDocument(document, {
      selection: range,
      preview: false
    });
    editor.revealRange(range, vscode.TextEditorRevealType.InCenter);
  }

  context.subscriptions.push(
    provider,
    view,
    vscode.commands.registerCommand('todoNavigator.refresh', refresh),
    vscode.commands.registerCommand('todoNavigator.filterType', chooseType),
    vscode.commands.registerCommand('todoNavigator.filterPriority', choosePriority),
    vscode.commands.registerCommand('todoNavigator.resetFilters', () => {
      provider.setTypeFilter('all');
      provider.setPriorityFilter('all');
      updateViewDescription();
    }),
    vscode.commands.registerCommand('todoNavigator.openTask', openTask),
    // Обновление после сохранения поддерживаемого файла в открытом проекте.
    vscode.workspace.onDidSaveTextDocument((document) => {
      if (SUPPORTED_FILE.test(document.uri.path) &&
          vscode.workspace.getWorkspaceFolder(document.uri)) {
        void refresh();
      }
    }),
    vscode.workspace.onDidChangeWorkspaceFolders(() => { void refresh(); })
  );

  // Первый поиск выполняется при активации расширения.
  void refresh();
}

function deactivate() { /* Подписки освобождаются через context.subscriptions. */ }

module.exports = { activate, deactivate };
