'use strict';

const vscode = require('vscode');
const { filterTasks } = require('./parser');

class FileNode {
  constructor(uri, tasks) {
    this.uri = uri;
    this.tasks = tasks;
  }
}

class TaskNode {
  constructor(task) {
    this.task = task;
  }
}

/** Данные для боковой панели: верхний уровень — файл, вложенный — задачи. */
class TaskTreeProvider {
  constructor() {
    this.allTasks = [];
    this.typeFilter = 'all';
    this.priorityFilter = 'all';
    this.changed = new vscode.EventEmitter();
    this.onDidChangeTreeData = this.changed.event;
  }

  dispose() {
    this.changed.dispose();
  }

  setTasks(tasks) {
    this.allTasks = tasks;
    this.changed.fire();
  }

  setTypeFilter(type) {
    this.typeFilter = type;
    this.changed.fire();
  }

  setPriorityFilter(priority) {
    this.priorityFilter = priority;
    this.changed.fire();
  }

  getVisibleCount() {
    return filterTasks(this.allTasks, this.typeFilter, this.priorityFilter).length;
  }

  getChildren(element) {
    if (element instanceof FileNode) {
      return element.tasks.map((task) => new TaskNode(task));
    }
    if (element) {
      return [];
    }

    const groups = new Map();
    const visible = filterTasks(this.allTasks, this.typeFilter, this.priorityFilter);

    for (const task of visible) {
      const key = task.uri.toString();
      if (!groups.has(key)) {
        groups.set(key, new FileNode(task.uri, []));
      }
      groups.get(key).tasks.push(task);
    }

    return [...groups.values()].sort((a, b) =>
      vscode.workspace.asRelativePath(a.uri, true)
        .localeCompare(vscode.workspace.asRelativePath(b.uri, true))
    );
  }

  getTreeItem(element) {
    if (element instanceof FileNode) {
      const item = new vscode.TreeItem(
        vscode.workspace.asRelativePath(element.uri, true),
        vscode.TreeItemCollapsibleState.Expanded
      );
      item.description = `${element.tasks.length} задач`;
      item.iconPath = new vscode.ThemeIcon('file-code');
      return item;
    }

    const task = element.task;
    const item = new vscode.TreeItem(
      `${task.type} [${task.priority}]: ${task.text}`,
      vscode.TreeItemCollapsibleState.None
    );
    item.description = `строка ${task.line + 1}`;
    item.tooltip = `${task.type} (${task.priority})\n${task.text}\nСтрока ${task.line + 1}`;
    item.iconPath = new vscode.ThemeIcon(task.type === 'FIXME' ? 'tools' : 'checklist');
    item.command = {
      command: 'todoNavigator.openTask',
      title: 'Перейти к задаче',
      arguments: [task]
    };
    return item;
  }
}

module.exports = { TaskTreeProvider };
