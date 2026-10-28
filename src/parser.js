'use strict';


const TASK_PATTERN = /^\s*\/\/\s*(TODO|FIXME)\s*\[\s*(high|medium|low)\s*\]\s*:\s*(\S.*?)\s*$/i;

// Возвращает задачи из текста одного файла номера строк начинаются с 0
function parseTasks(text) {
  const result = [];
  const lines = text.split(/\r?\n/);

  lines.forEach((line, lineNumber) => {
    const match = line.match(TASK_PATTERN);
    if (!match) {
      return;
    }

    result.push({
      type: match[1].toUpperCase(),
      priority: match[2].toLowerCase(),
      text: match[3].trim(),
      line: lineNumber
    });
  });

  return result;
}

/** Применяет два независимых фильтра к найденным задачам. */
function filterTasks(tasks, type, priority) {
  return tasks.filter((task) =>
    (type === 'all' || task.type === type) &&
    (priority === 'all' || task.priority === priority)
  );
}

module.exports = { parseTasks, filterTasks };
